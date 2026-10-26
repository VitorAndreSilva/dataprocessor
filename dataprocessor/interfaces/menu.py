from ..infra.fontes import FonteDadosArquivos
from ..services.processamento import executar_processamento
from ..infra.relatorios import criar_gerador

def processar_caminhos(caminho_partidas, caminho_times, caminho_config):
    fonte = FonteDadosArquivos(caminho_partidas, caminho_times, caminho_config)
    return executar_processamento(fonte)

def processar():
    caminho_partidas = input("Caminho do CSV de clientes [data/matches_original.csv]: ").strip() or "data/matches_original.csv"
    caminho_times = input("Caminho do CSV de transações [data/teams_world_cup_2026.csv]: ").strip() or "data/teams_world_cup_2026.csv"
    caminho_config = input("Caminho do JSON de config [data/config.json]: ").strip() or "data/config.json"

    try:
        resultado = processar_caminhos(caminho_partidas, caminho_times, caminho_config)
    except (OSError, ValueError, KeyError) as erro:
        print(f"[ERRO] Não foi possível processar: {erro}")
        return None
    print(f"Partidas válidas: {len(resultado["total_jogos"])}")
    print(f"Equipes válidas: {len(resultado["equipes"])}")
    return resultado

def exibir(resultado, formato_padrao):
    formatos = {"texto", "json", "csv"}
    formato = input(f"Formato (texto/json/csv) [{formato_padrao}]: ").strip() or formato_padrao
    if formato not in formatos:
        print(f"Formato inválido: {formato}")
        return
    try:
        gerador = criar_gerador(formato)
    except (OSError, ValueError, KeyError) as erro:
        print(f"[ERRO] A exibição falhou: {erro}")
        return None
    print(gerador.render(resultado))
    return formato_padrao