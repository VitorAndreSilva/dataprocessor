from abc import ABC, abstractmethod
from dataprocessor.core.entities import Equipe, Partida
from dataprocessor.infra.arquivos import carregar_partidas, carregar_equipes, carregar_config

class FonteDados(ABC):
    @abstractmethod
    def carregar_partidas(self) -> list[Partida]: ...

    @abstractmethod
    def carregar_equipes(self) -> list[Equipe]: ...

    @abstractmethod
    def carregar_config(self) -> dict: ...

class FonteDadosArquivos(FonteDados):
    def __init__(self, caminho_partidas, caminho_equipes, caminho_config):
        self.carregar_partidas = caminho_partidas
        self.carregar_equipes = caminho_equipes
        self.carregar_config = caminho_config

    def carregar_partidas(self):
        return carregar_partidas(self.caminho_partidas)

    def carregar_equipes(self):
        return carregar_equipes(self.caminho_equipes)

    def carregar_config(self):
        return carregar_config(self.caminho_config)