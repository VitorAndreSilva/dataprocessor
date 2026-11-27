import unittest

from dataprocessor.core.entities import Equipe, Partida
from dataprocessor.infra.fontes import FonteDadosArquivos, FonteDadosMemoria
from dataprocessor.services.processamento import executar_processamento

try:
    from fastapi.testclient import TestClient

    from dataprocessor.interfaces.api import app, obter_fonte
except ImportError:
    TestClient = None

CONFIG = {
    "status_validos": ["FINISHED", "SCHEDULED"],
    "estagios_validos": ["GROUP_STAGE"],
}


def fonte_de_teste():
    return FonteDadosMemoria(
        partidas=[
            Partida("2026-06-11", "Mexico", "South Africa", 2, 0),
            Partida("2026-06-12", "South Korea", "Czechia", 2, 1),
            Partida("", "", "", None, None),
        ],
        equipes=[
            Equipe("Mexico", "MEX"),
            Equipe("South Africa", "RSA"),
            Equipe("", ""),
        ],
        config=CONFIG,
    )


@unittest.skipIf(TestClient is None, "fastapi não instalado")
class ApiTestCase(unittest.TestCase):
    def setUp(self):
        app.dependency_overrides[obter_fonte] = fonte_de_teste
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()

    def test_metricas(self):
        corpo = self.client.get("/metricas").json()
        self.assertEqual(corpo["partidas_validas"], 2)
        self.assertEqual(corpo["partidas_invalidas"], 1)
        self.assertEqual(corpo["equipes_validas"], 2)
        self.assertEqual(corpo["equipes_invalidas"], 1)
        self.assertEqual(corpo["media_gols"], 1.25)
        self.assertEqual(corpo["total_equipes"], 2)

    def test_lista_somente_registros_validos(self):
        equipes = self.client.get("/equipes").json()
        partidas = self.client.get("/partidas").json()
        self.assertEqual(len(equipes), 2)
        self.assertEqual(len(partidas), 2)

    def test_equipe_encontrada_devolve_200(self):
        resposta = self.client.get("/equipes/MEX")
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json()["nome"], "Mexico")

    def test_equipe_inexistente_devolve_404(self):
        resposta = self.client.get("/equipes/XXX")
        self.assertEqual(resposta.status_code, 404)
        self.assertIn("XXX", resposta.json()["detail"])

    def test_formato_invalido_devolve_422(self):
        self.assertEqual(self.client.get("/relatorio/xml").status_code, 422)

    def test_gols_min_nao_numerico_devolve_422(self):
        self.assertEqual(self.client.get("/partidas", params={"gols_min": "abc"}).status_code, 422)

    def test_filtra_partidas_por_data(self):
        corpo = self.client.get("/partidas", params={"data": "2026-06-11"}).json()
        self.assertEqual([p["equipe_casa"] for p in corpo], ["Mexico"])

    def test_relatorio_csv_tem_content_type(self):
        resposta = self.client.get("/relatorio/csv")
        self.assertTrue(resposta.headers["content-type"].startswith("text/csv"))

    def test_fonte_indisponivel_devolve_503(self):
        app.dependency_overrides[obter_fonte] = lambda: FonteDadosArquivos("x.csv", "y.csv", "z.json")
        resposta = self.client.get("/metricas")
        self.assertEqual(resposta.status_code, 503)
        self.assertIn("indisponível", resposta.json()["detail"])

    def test_metricas_identicas_ao_service(self):
        direto = executar_processamento(fonte_de_teste())
        corpo = self.client.get("/metricas").json()
        self.assertEqual(corpo["media_gols"], direto.media_gols)
        self.assertEqual(corpo["total_equipes"], direto.total_equipes)


@unittest.skipIf(TestClient is None, "fastapi não instalado")
class ProcessarTestCase(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def corpo(self, **mudancas):
        base = {
            "partidas": [
                {
                    "data": "2026-06-11",
                    "equipe_casa": "Mexico",
                    "equipe_fora": "South Africa",
                    "gols_casa": 2,
                    "gols_fora": 0,
                }
            ],
            "equipes": [{"nome": "Mexico", "sigla": "MEX"}],
            "config": CONFIG,
        }
        base.update(mudancas)
        return base

    def test_processa_corpo_valido(self):
        resposta = self.client.post("/processar", json=self.corpo())
        self.assertEqual(resposta.status_code, 200)
        corpo = resposta.json()
        self.assertEqual(corpo["media_gols"], 1.0)
        self.assertEqual(corpo["total_equipes"], 1)

    def test_regra_de_negocio_ainda_vem_do_core(self):
        partida = {
            "data": "2026-06-11",
            "equipe_casa": "",
            "equipe_fora": "South Africa",
            "gols_casa": 2,
            "gols_fora": 0,
        }
        corpo = self.client.post("/processar", json=self.corpo(partidas=[partida])).json()
        self.assertEqual(corpo["partidas_invalidas"], 1)

    def test_corpo_mal_formado_devolve_422(self):
        resposta = self.client.post("/processar", json={"partidas": "nao-e-lista"})
        self.assertEqual(resposta.status_code, 422)


if __name__ == "__main__":
    unittest.main()
