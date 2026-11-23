import json
import unittest

from dataprocessor.core.entities import Equipe, Partida
from dataprocessor.core.resultados import ResultadoProcessamento
from dataprocessor.infra.relatorios import (
    GeradorRelatorio,
    RelatorioCsv,
    RelatorioJson,
    RelatorioTexto,
)


def resultado_exemplo():
    return ResultadoProcessamento(
        partidas=(
            Partida("2026-06-11", "Mexico", "South Africa", 2, 0),
        ),
        equipes=(
            Equipe("Algeria", "ALG"),
        ),
        partidas_invalidas=(),
        equipes_invalidas=(),
        media_gols=1.54,
        total_equipes=48,
    )


class RelatoriosTestCase(unittest.TestCase):
    def test_gerador_relatorio_e_uma_abc(self):
        self.assertTrue(issubclass(RelatorioTexto, GeradorRelatorio))

        with self.assertRaises(TypeError):
            GeradorRelatorio()

        class GeradorIncompleto(GeradorRelatorio):
            pass

        with self.assertRaises(TypeError):
            GeradorIncompleto()

    def test_relatorio_texto_exibe_metricas(self):
        texto = RelatorioTexto().render(resultado_exemplo())

        self.assertIn("Partidas válidas: 1", texto)
        self.assertIn("Média de gols: 1.54", texto)
        self.assertIn("Total de equipes: 48", texto)

    def test_relatorio_json_preserva_dados_do_resultado(self):
        documento = json.loads(RelatorioJson().render(resultado_exemplo()))

        self.assertEqual(documento["partidas"][0]["equipe_casa"], "Mexico")
        self.assertEqual(documento["metricas"]["media_gols"], 1.54)

    def test_relatorio_csv_produz_cabecalho_e_linhas(self):
        conteudo = RelatorioCsv().render(resultado_exemplo())

        self.assertIn("data,equipe_casa,equipe_fora,gols_casa,gols_fora", conteudo)
        self.assertIn("2026-06-11,Mexico,South Africa,2,0", conteudo)


if __name__ == "__main__":
    unittest.main()
