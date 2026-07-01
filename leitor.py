import os, csv, json

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
            partidas.append({
                "data": linha["utcDate"],
                "equipe_casa": linha["homeTeam.name"],
                "equipe_visitante": linha["awayTeam.name"],
                "gols_casa": _para_int(linha["score.fullTime.home"]),
                "gols_fora": _para_int(linha["score.fullTime.away"])
            })

        return partidas

def carregar_config(caminho):
    if not os.path.exists(caminho):
        print(f"ERRO: Arquivo não encontrado: {caminho}")
        return []
    
    with open(caminho, encoding="utf-8") as arquivo:
        json.load(caminho)