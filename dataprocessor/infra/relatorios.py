from abc import ABC, abstractmethod
import csv
import io
import json

from ..core.resultados import ResultadoProcessamento


class GeradorRelatorio(ABC):
    @abstractmethod
    def render(self, resultado: ResultadoProcessamento) -> str:
        ...


class RelatorioTexto(GeradorRelatorio):
    def render(self, resultado: ResultadoProcessamento) -> str:
        return "\n".join(
            [
                "=== DataProcessor Copa do Mundo 2026 ===",
                "",
                "[VALIDAÇÃO]",
                f"Partidas válidas: {len(resultado.partidas)}",
                f"Partidas inválidas: {len(resultado.partidas_invalidas)}",
                f"Equipes válidas: {len(resultado.equipes)}",
                f"Equipes inválidas: {len(resultado.equipes_invalidas)}",
                "",
                "[RELATÓRIO]",
                f"Média de gols: {resultado.media_gols:.2f}",
                f"Total de equipes: {resultado.total_equipes}",
            ]
        )


class RelatorioJson(GeradorRelatorio):
    def render(self, resultado: ResultadoProcessamento) -> str:
        return json.dumps(resultado.to_dict(), ensure_ascii=False, indent=2) + "\n"


class RelatorioCsv(GeradorRelatorio):
    def render(self, resultado: ResultadoProcessamento) -> str:
        arquivo = io.StringIO()
        escritor = csv.writer(arquivo, lineterminator="\n")
        escritor.writerow(("data", "equipe_casa", "equipe_fora", "gols_casa", "gols_fora"))
        for partida in resultado.partidas:
            escritor.writerow(
                (partida.data, partida.equipe_casa, partida.equipe_fora, partida.gols_casa, partida.gols_fora)
            )
        return arquivo.getvalue()


def criar_gerador(formato: str) -> GeradorRelatorio:
    geradores = {
        "texto": RelatorioTexto,
        "json": RelatorioJson,
        "csv": RelatorioCsv,
    }
    return geradores[formato]()
