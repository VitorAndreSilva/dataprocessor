from abc import abstractmethod, ABC
import json

class GeradorRelatorio(ABC):
    @abstractmethod
    def render(self, resultado) -> str:
        ...

class RelatorioTexto:
    def render(self, resultado) -> str:
        return "\n".join(
            [
                "=== DataProcessor Copa do Mundo 2026 ===",
                f"Jogos válidos: {len(resultado.jogos)}"
                f"Média de gols: {resultado.media_gols}"
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