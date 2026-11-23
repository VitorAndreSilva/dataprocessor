from dataclasses import dataclass


@dataclass(frozen=True)
class Partida:
    data: str
    equipe_casa: str
    equipe_fora: str
    gols_casa: int | None
    gols_fora: int | None

    @property
    def identificacao(self) -> str:
        return f"{self.equipe_casa} x {self.equipe_fora}"


@dataclass(frozen=True)
class Equipe:
    nome: str
    sigla: str

    @property
    def identificacao(self) -> str:
        return f"{self.nome} ({self.sigla})"
