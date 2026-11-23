from fastapi import FastAPI, Response

from ..infra.fontes import fonte_a_partir_de_caminhos
from ..infra.relatorios import criar_gerador
from ..services.processamento import executar_processamento

app = FastAPI(title="FIFA World Cup - DataProcessor API")


def carregar_resultado():
    fonte = fonte_a_partir_de_caminhos(
        "data/matches_original.csv",
        "data/times.csv",
        "data/config.json",
    )
    return executar_processamento(fonte)


@app.get("/relatorio")
def relatorio():
    return carregar_resultado().to_dict()


@app.get("/relatorio/csv")
def relatorio_csv():
    conteudo = criar_gerador("csv").render(carregar_resultado())
    return Response(content=conteudo, media_type="text/csv")
