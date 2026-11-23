import csv
import json

from dataprocessor.core.entities import Equipe, Partida


def _para_float(valor, padrao=None):
    try:
        return float(valor)
    except (TypeError, ValueError):
        return padrao


def _para_int(valor, padrao=None):
    try:
        return int(valor)
    except (TypeError, ValueError):
        try:
            return int(_para_float(valor))
        except (TypeError, ValueError):
            return padrao


def carregar_partidas(caminho):
    partidas = []
    with open(caminho, encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            partida = Partida(
                data=linha["utcDate"],
                equipe_casa=linha["homeTeam.name"],
                equipe_fora=linha["awayTeam.name"],
                gols_casa=_para_int(linha["score.fullTime.home"]),
                gols_fora=_para_int(linha["score.fullTime.away"]),
            )
            partidas.append(partida)
    return partidas


def carregar_equipes(caminho):
    equipes = []
    with open(caminho, encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            equipe = Equipe(
                nome=linha["name"],
                sigla=linha["tla"],
            )
            equipes.append(equipe)
    return equipes


def carregar_config(caminho):
    with open(caminho, encoding="utf-8") as arquivo:
        return json.load(arquivo)
