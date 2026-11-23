from dataclasses import asdict

from fastapi import FastAPI, Response

from ..infra.fontes import fonte_a_partir_de_caminhos
from ..infra.relatorios import criar_gerador
from ..services.processamento import executar_processamento

app = FastAPI(title="FIFA World Cup - DataProcessor API")
MEDIA_TYPES = {"texto": "text/plain", "json": "application/json", "csv": "text/csv"}

def carregar_resultado():
    fonte = fonte_a_partir_de_caminhos(
        "data/matches_original.csv",
        "data/times.csv",
        "data/config.json",
    )
    return executar_processamento(fonte)

@app.get("/matches")
def listar_clientes():
    resultado = carregar_resultado()
    return [asdict(cliente) for cliente in resultado.clientes]

@app.get("/metricas")
def metricas():
    resultado = carregar_resultado()
    return {
        "media_gols": resultado.media_idade,
        "total_aprovado": resultado.total_aprovado,
    }

@app.get("/transacoes")
def listar_transacoes(status: str | None = None, categoria: str | None = None):
    transacoes = carregar_resultado().transacoes
    if status is not None:
        transacoes = [t for t in transacoes if t.status == status]
    if categoria is not None:
        transacoes = [t for t in transacoes if t.categoria == categoria]
    return [asdict(t) for t in transacoes]



@app.get("/relatorio/{formato}")
def relatorio_formatado(formato: str):
    conteudo = criar_gerador(formato).render(carregar_resultado())
    return Response(content=conteudo, media_type=MEDIA_TYPES[formato])