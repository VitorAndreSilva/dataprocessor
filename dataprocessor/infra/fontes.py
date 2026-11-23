from abc import ABC, abstractmethod

from dataprocessor.core.entities import Equipe, Partida
from dataprocessor.infra.arquivos import carregar_config, carregar_equipes, carregar_partidas


class FonteDados(ABC):
    @abstractmethod
    def carregar_partidas(self) -> list[Partida]: ...

    @abstractmethod
    def carregar_equipes(self) -> list[Equipe]: ...

    @abstractmethod
    def carregar_config(self) -> dict: ...


class FonteDadosArquivos(FonteDados):
    def __init__(self, caminho_partidas, caminho_equipes, caminho_config):
        self.caminho_partidas = caminho_partidas
        self.caminho_equipes = caminho_equipes
        self.caminho_config = caminho_config

    def carregar_partidas(self):
        return carregar_partidas(self.caminho_partidas)

    def carregar_equipes(self):
        return carregar_equipes(self.caminho_equipes)

    def carregar_config(self):
        return carregar_config(self.caminho_config)


class FonteDadosMemoria(FonteDados):
    def __init__(self, partidas=(), equipes=(), config=None):
        self._partidas = tuple(partidas)
        self._equipes = tuple(equipes)
        self._config = dict(config or {})

    def carregar_partidas(self):
        return list(self._partidas)

    def carregar_equipes(self):
        return list(self._equipes)

    def carregar_config(self):
        return dict(self._config)


def fonte_a_partir_de_caminhos(caminho_partidas, caminho_equipes, caminho_config) -> FonteDados:
    return FonteDadosArquivos(caminho_partidas, caminho_equipes, caminho_config)
