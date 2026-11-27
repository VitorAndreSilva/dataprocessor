from pydantic import BaseModel, ConfigDict


class PartidaSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    data: str
    equipe_casa: str
    equipe_fora: str
    gols_casa: int | None
    gols_fora: int | None


class EquipeSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nome: str
    sigla: str


class MetricasSchema(BaseModel):
    partidas_validas: int
    partidas_invalidas: int
    equipes_validas: int
    equipes_invalidas: int
    media_gols: float
    total_equipes: int


class PartidaEntrada(BaseModel):
    data: str
    equipe_casa: str
    equipe_fora: str
    gols_casa: int | None = None
    gols_fora: int | None = None


class EquipeEntrada(BaseModel):
    nome: str
    sigla: str = ""


class ConfigEntrada(BaseModel):
    status_validos: list[str] = []
    estagios_validos: list[str] = []


class ProcessamentoEntrada(BaseModel):
    partidas: list[PartidaEntrada]
    equipes: list[EquipeEntrada]
    config: ConfigEntrada
