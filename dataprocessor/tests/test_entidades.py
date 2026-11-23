import unittest

from dataprocessor.core.entities import Equipe, Partida


class PartidaTestCase(unittest.TestCase):
    def test_partida_exibe_identificacao_derivada(self):
        partida = Partida(
            data="2026-06-11",
            equipe_casa="Mexico",
            equipe_fora="South Africa",
            gols_casa=2,
            gols_fora=0,
        )

        self.assertEqual(partida.identificacao, "Mexico x South Africa")


class EquipeTestCase(unittest.TestCase):
    def test_equipe_exibe_identificacao_derivada(self):
        equipe = Equipe(nome="Algeria", sigla="ALG")

        self.assertEqual(equipe.identificacao, "Algeria (ALG)")

    def test_entidades_sao_imutaveis(self):
        partida = Partida("2026-06-11", "Mexico", "South Africa", 2, 0)

        with self.assertRaises(AttributeError):
            partida.gols_casa = 3


if __name__ == "__main__":
    unittest.main()
