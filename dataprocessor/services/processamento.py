from ..infra.arquivos import carregar_partidas, carregar_config
from ..core.metricas import media_gols
from ..core.validador import validar_partida, separar_registros
from ..core.transformador import transformar_partidas

def executar_processamento(app_config):
    # Carregar
    partidas_raw = carregar_partidas(app_config.caminho_jogos)
    config = carregar_config(app_config.caminho_config)
    # Validar
    jogos_validos, jogos_invalidos = separar_registros(partidas_raw, validar_partida)
    total_jogos = jogos_validos + jogos_invalidos
    # Processar
    media = media_gols(jogos_validos)
    #soma = soma_gols(jogos_validos)
    # Transformar
    partidas = transformar_partidas(jogos_validos)

    return {
        "total_jogos": total_jogos,
        "jogos_validos": jogos_validos,
        "jogos_invalidos": jogos_invalidos,
        "media_gols": media,
        #"soma_gols": soma,
        "partidas": partidas
    }