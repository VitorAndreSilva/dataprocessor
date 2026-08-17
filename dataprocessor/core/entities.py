from dataclasses import dataclass

@dataclass(frozen=True)
class Partida:
    #id: int
    data: str
    equipe_casa: str
    equipe_fora: str
    gols_casa: str
    gols_fora: str

    @property
    def identificacao(self) -> str:
        return f"{self.equipe_casa} x {self.equipe_fora}"