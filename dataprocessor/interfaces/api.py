from typing import Literal

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse

from ..core.entities import Equipe, Partida
from ..core.resultados import ResultadoProcessamento
from ..infra.fontes import FonteDados, FonteDadosMemoria, fonte_a_partir_de_caminhos
from ..infra.relatorios import criar_gerador
from ..services.processamento import executar_processamento
from .config import Settings, obter_settings
from .schemas import (
    EquipeSchema,
    MetricasSchema,
    PartidaSchema,
    ProcessamentoEntrada,
)

app = FastAPI(title="FIFA World Cup - DataProcessor API")

MEDIA_TYPES = {"texto": "text/plain", "json": "application/json", "csv": "text/csv"}


@app.exception_handler(OSError)
def fonte_indisponivel(request: Request, erro: OSError) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={"detail": f"Fonte de dados indisponível: {erro}"},
    )


def obter_fonte(settings: Settings = Depends(obter_settings)) -> FonteDados:
    pasta = settings.data_dir
    return fonte_a_partir_de_caminhos(
        pasta / "matches_original.csv",
        pasta / "times.csv",
        pasta / "config.json",
    )


def obter_resultado(fonte: FonteDados = Depends(obter_fonte)) -> ResultadoProcessamento:
    return executar_processamento(fonte)


def resumir(resultado: ResultadoProcessamento) -> MetricasSchema:
    return MetricasSchema(
        partidas_validas=len(resultado.partidas),
        partidas_invalidas=len(resultado.partidas_invalidas),
        equipes_validas=len(resultado.equipes),
        equipes_invalidas=len(resultado.equipes_invalidas),
        media_gols=resultado.media_gols,
        total_equipes=resultado.total_equipes,
    )


@app.get("/relatorio")
def relatorio(resultado: ResultadoProcessamento = Depends(obter_resultado)):
    return resultado.to_dict()


@app.get("/equipes", response_model=list[EquipeSchema])
def listar_equipes(resultado: ResultadoProcessamento = Depends(obter_resultado)):
    return resultado.equipes


@app.get("/partidas", response_model=list[PartidaSchema])
def listar_partidas(
    data: str | None = None,
    equipe: str | None = None,
    gols_min: int | None = None,
    resultado: ResultadoProcessamento = Depends(obter_resultado),
):
    partidas = resultado.partidas
    if data is not None:
        partidas = [partida for partida in partidas if partida.data == data]
    if equipe is not None:
        partidas = [
            partida
            for partida in partidas
            if equipe in (partida.equipe_casa, partida.equipe_fora)
        ]
    if gols_min is not None:
        partidas = [
            partida
            for partida in partidas
            if (partida.gols_casa + partida.gols_fora) >= gols_min
        ]
    return partidas


@app.get("/metricas", response_model=MetricasSchema)
def metricas(resultado: ResultadoProcessamento = Depends(obter_resultado)):
    return resumir(resultado)


@app.get("/relatorio/{formato}")
def relatorio_formatado(
    formato: Literal["texto", "json", "csv"],
    resultado: ResultadoProcessamento = Depends(obter_resultado),
):
    conteudo = criar_gerador(formato).render(resultado)
    return Response(content=conteudo, media_type=MEDIA_TYPES[formato])


@app.get("/equipes/{sigla}", response_model=EquipeSchema)
def obter_equipe(sigla: str, resultado: ResultadoProcessamento = Depends(obter_resultado)):
    for equipe in resultado.equipes:
        if equipe.sigla == sigla:
            return equipe
    raise HTTPException(status_code=404, detail=f"Equipe {sigla} não encontrada")


@app.post("/processar", response_model=MetricasSchema)
def processar(entrada: ProcessamentoEntrada):
    fonte = FonteDadosMemoria(
        partidas=[Partida(**partida.model_dump()) for partida in entrada.partidas],
        equipes=[Equipe(**equipe.model_dump()) for equipe in entrada.equipes],
        config=entrada.config.model_dump(),
    )
    return resumir(executar_processamento(fonte))
