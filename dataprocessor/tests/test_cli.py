import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class CliTestCase(unittest.TestCase):
    def test_cli_salva_relatorio_json_e_log(self):
        projeto = Path(__file__).resolve().parents[2]
        with tempfile.TemporaryDirectory() as pasta:
            saida = Path(pasta)
            processo = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "dataprocessor",
                    "--partidas",
                    str(projeto / "data/matches_original.csv"),
                    "--times",
                    str(projeto / "data/times.csv"),
                    "--config",
                    str(projeto / "data/config.json"),
                    "--formato",
                    "json",
                    "--output",
                    str(saida),
                ],
                cwd=projeto,
                capture_output=True,
                text=True,
            )

            self.assertEqual(processo.returncode, 0, processo.stderr)
            relatorio = json.loads((saida / "relatorio.json").read_text(encoding="utf-8"))
            self.assertEqual(relatorio["metricas"]["media_gols"], 1.54)
            self.assertTrue((saida / "dataprocessor.log").exists())

    def test_cli_caminho_invalido_retorna_codigo_1(self):
        projeto = Path(__file__).resolve().parents[2]
        with tempfile.TemporaryDirectory() as pasta:
            processo = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "dataprocessor",
                    "--partidas",
                    "nao-existe.csv",
                    "--times",
                    str(projeto / "data/times.csv"),
                    "--config",
                    str(projeto / "data/config.json"),
                    "--output",
                    pasta,
                ],
                cwd=projeto,
                capture_output=True,
                text=True,
            )

            self.assertEqual(processo.returncode, 1)
            self.assertIn("[ERRO]", processo.stdout)


if __name__ == "__main__":
    unittest.main()
