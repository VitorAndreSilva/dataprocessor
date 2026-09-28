from ..infra.fontes import FonteDadosArquivos
from ..services.processamento import executar_processamento
from ..infra.relatorios import criar_gerador

def processar():
    caminho_partidas = input("Caminho do CSV de clientes [data/matches_original.csv]: ").strip() or "data/matches_original.csv"
    caminho_times = input("Caminho do CSV de transações [data/teams_world_cup_2026.csv]: ").strip() or "data/teams_world_cup_2026.csv"
    caminho_config = input("Caminho do JSON de config [data/config.json]: ").strip() or "data/config.json"

    fonte = FonteDadosArquivos(caminho_partidas, caminho_times, caminho_config)
    resultado = executar_processamento(fonte)
    print(f"Partidas válidas: {len(resultado["total_jogos"])}")
    print(f"Equipes válidas: {len(resultado["equipes"])}")
    return resultado

def exibir(resultado):
    formato = input("Formato (texto/json/csv) [texto]: ").strip() or "texto"
    gerador = criar_gerador(formato)
    print(gerador.render(resultado))