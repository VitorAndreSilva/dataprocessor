from dataclasses import dataclass

@dataclass(frozen=True)
class AppConfig:
    caminho_jogos: str
    caminho_config: str
    caminho_equipes: str

def carregamento_configuracao_padrao():
    return AppConfig(
        caminho_jogos="data/matches_original.csv",
        caminho_config="data/config.json",
        caminho_equipes="data/teams_world_cup_2026.csv"
    )