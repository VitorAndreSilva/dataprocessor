import unittest

from dataprocessor.interfaces.menu import processar_caminhos

class ProcessarCaminhosTestCase(unittest.TestCase):
    def test_processa_dataset_padrao(self):
        resultado = processar_caminhos(
            "data/matches_original.csv",
            "data/times.csv",
            "data/config.json",
        )
        self.assertEqual(resultado["media_gols"], 1.54)