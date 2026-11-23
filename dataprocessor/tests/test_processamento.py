import unittest
from pathlib import Path

from dataprocessor.core.entities import Equipe, Partida
from dataprocessor.infra.fontes import FonteDados, FonteDadosArquivos, FonteDadosMemoria
from dataprocessor.services.processamento import executar_processamento


class ProcessamentoTestCase(unittest.TestCase):
    def test_fonte_dados_e_uma_abc(self):
        self.assertTrue(issubclass(FonteDadosArquivos, FonteDados))
        self.assertTrue(issubclass(FonteDadosMemoria, FonteDados))

        with self.assertRaises(TypeError):
            FonteDados()

        class FonteIncompleta(FonteDados):
            pass

        with self.assertRaises(TypeError):
            FonteIncompleta()

    def test_dataset_oficial_preserva_metricas(self):
        data = Path(__file__).resolve().parents[2] / "data"
        resultado = executar_processamento(
            FonteDadosArquivos(data / "matches_original.csv", data / "times.csv", data / "config.json")
        )

        self.assertEqual(resultado.media_gols, 1.54)
        self.assertEqual(resultado.total_equipes, 48)

    def test_service_aceita_fonte_em_memoria(self):
        fonte = FonteDadosMemoria(
            partidas=(
                Partida("2026-06-11T20:00:00Z", "Mexico", "South Africa", 2, 0),
            ),
            equipes=(
                Equipe("  algeria ", "alg"),
            ),
            config={"status_validos": ["FINISHED"]},
        )

        resultado = executar_processamento(fonte)

        self.assertEqual(len(resultado.partidas), 1)
        self.assertEqual(resultado.partidas[0].data, "2026-06-11")
        self.assertEqual(resultado.equipes[0].nome, "Algeria")
        self.assertEqual(resultado.equipes[0].sigla, "ALG")
        self.assertEqual(resultado.total_equipes, 1)


if __name__ == "__main__":
    unittest.main()
