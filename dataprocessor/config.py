from dataclasses import dataclass

@dataclass(frozen=True)
class AppConfig:
    caminho_jogos: str
    caminho_config: str

def carregamento_configuracao_padrao():
    return AppConfig(
        caminho_jogos="data/matches_original.csv",
        caminho_config="data/config.json"
    )