from dataclasses import asdict, dataclass
from typing import Any

from .entities import Equipe, Partida


@dataclass(frozen=True)
class RegistroInvalido:
    registro: Partida | Equipe
    erros: tuple[str, ...]

    @property
    def identificacao(self) -> str:
        return self.registro.identificacao


@dataclass(frozen=True)
class ResultadoProcessamento:
    partidas: tuple[Partida, ...]
    equipes: tuple[Equipe, ...]
    partidas_invalidas: tuple[RegistroInvalido, ...]
    equipes_invalidas: tuple[RegistroInvalido, ...]
    media_gols: float
    total_equipes: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "partidas": [asdict(partida) for partida in self.partidas],
            "equipes": [asdict(equipe) for equipe in self.equipes],
            "partidas_invalidas": [
                {"registro": asdict(item.registro), "erros": list(item.erros)}
                for item in self.partidas_invalidas
            ],
            "equipes_invalidas": [
                {"registro": asdict(item.registro), "erros": list(item.erros)}
                for item in self.equipes_invalidas
            ],
            "metricas": {
                "media_gols": self.media_gols,
                "total_equipes": self.total_equipes,
            },
        }
