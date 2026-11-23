from ..core.metricas import media_gols, soma_equipes
from ..core.resultados import ResultadoProcessamento
from ..core.transformador import transformar_equipes, transformar_partidas
from ..core.validador import separar_registros, validar_equipe, validar_partida
from ..infra.fontes import FonteDados


def executar_processamento(fonte: FonteDados) -> ResultadoProcessamento:
    # Carregar
    partidas_raw = fonte.carregar_partidas()
    equipes_raw = fonte.carregar_equipes()
    config = fonte.carregar_config()
    # Validar
    partidas_validas, partidas_invalidas = separar_registros(partidas_raw, validar_partida)
    equipes_validas, equipes_invalidas = separar_registros(equipes_raw, validar_equipe)
    # Transformar
    partidas = transformar_partidas(partidas_validas)
    equipes = transformar_equipes(equipes_validas)
    # Processar
    return ResultadoProcessamento(
        partidas=tuple(partidas),
        equipes=tuple(equipes),
        partidas_invalidas=tuple(partidas_invalidas),
        equipes_invalidas=tuple(equipes_invalidas),
        media_gols=media_gols(partidas),
        total_equipes=soma_equipes(equipes),
    )
