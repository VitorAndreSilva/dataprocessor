from ..infra.arquivos import carregar_partidas, carregar_config, carregar_equipes
from ..core.metricas import media_gols, soma_equipes
from ..core.validador import validar_partida, separar_registros, validar_equipe
from ..core.transformador import transformar_partidas, transformar_equipes

def executar_processamento(app_config):
    # Carregar
    partidas_raw = carregar_partidas(app_config.carregar_partidas)
    equipes_raw = carregar_equipes(app_config.carregar_equipes)
    config = carregar_config(app_config.carregar_config)
    # Validar
    jogos_validos, jogos_invalidos = separar_registros(partidas_raw, validar_partida)
    total_jogos = jogos_validos + jogos_invalidos
    equipes_validas, equipes_invalidas = separar_registros(equipes_raw, validar_equipe)
    # Processar
    media = media_gols(jogos_validos)
    total_equipes = soma_equipes(equipes_validas)
    # Transformar
    partidas = transformar_partidas(jogos_validos)
    equipes = transformar_equipes(equipes_validas)

    return {
        "total_jogos": total_jogos,
        "jogos_validos": jogos_validos,
        "jogos_invalidos": jogos_invalidos,
        "media_gols": media,
        #"soma_gols": soma,
        "partidas": partidas,
        "equipes": equipes,
        "total_equipes": total_equipes
    }