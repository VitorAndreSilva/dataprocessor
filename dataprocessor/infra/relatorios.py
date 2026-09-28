from abc import abstractmethod, ABC
import json, io, csv

class GeradorRelatorio(ABC):
    @abstractmethod
    def render(self, resultado) -> str:
        ...

class RelatorioTexto:
    def render(self, resultado) -> str:
        return "\n".join(
            [
                "=== DataProcessor Copa do Mundo 2026 ===",
                f"Jogos válidos: {len(resultado["partidas"])} "
                f"Média de gols: {resultado["media_gols"]}"
            ]
        )

class RelatorioJSON:
    def render(self, resultado) -> str:
        return json.dumps(resultado.to_dict(), ensure_ascii=False, indent=2) + '\n'

    def criador_gerador(formato: str) -> GeradorRelatorio:
        geradores = {
            "texto": RelatorioTexto,
            "json": RelatorioJSON
        }
        return geradores[formato]

class RelatorioCSV:
    def render(self, resultado) -> str:
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
        "json": RelatorioJSON,
        "csv": RelatorioCSV
    }
    return geradores[formato]()