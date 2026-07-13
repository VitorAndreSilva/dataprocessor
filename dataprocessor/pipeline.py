from .leitor import carregar_partidas, carregar_config
from .processador import media_gols
from .validador import validar_partida, separar_registros
from .transformador import transformar_partidas

def executar_pipeline(caminho_partidas, caminho_config):
    # Carregar
    partidas_raw = carregar_partidas(caminho_partidas)
    config = carregar_config(caminho_config)
    # Validar
    jogos_validos, jogos_invalidos = separar_registros(partidas_raw, validar_partida)
    total_jogos = jogos_validos + jogos_invalidos
    # Processar
    media = media_gols(jogos_validos)
    # Transformar
    partidas = transformar_partidas(jogos_validos)

    return {
        "total_jogos": total_jogos,
        "jogos_validos": jogos_validos,
        "jogos_invalidos": jogos_invalidos,
        "media_gols": media,
        "partidas": partidas
    }