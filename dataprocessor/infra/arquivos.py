import os, csv, json
from dataprocessor.core.entities import Partida

def _para_float(valor, padrao=None):
    try:
        valor = float(valor)
        return valor
    except:
        return None    

def _para_int(valor, padrao=None):
    try:
        valor = int(_para_float(valor))
        return valor
    except:
        return None

def carregar_partidas(caminho):
    if not os.path.exists:
        print(f"ERRO: Arquivo não encontrado: {caminho}")
        return []
    
    partidas = []
    with open(caminho, encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            partida = Partida(
                #id=_para_int(linha["id"]),
                data=linha["utcDate"],
                equipe_casa=linha["homeTeam.name"],
                equipe_fora=linha["awayTeam.name"],
                gols_casa=_para_int(linha["score.fullTime.home"]),
                gols_fora=_para_int(linha["score.fullTime.away"])
            )
            partidas.append(partida)

        return partidas

def carregar_config(caminho):
    if not os.path.exists(caminho):
        print(f"ERRO: Arquivo não encontrado: {caminho}")
        return []
    
    with open(caminho, encoding="utf-8") as arquivo:
        return json.load(arquivo)