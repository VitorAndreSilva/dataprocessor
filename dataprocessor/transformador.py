import unicodedata
from datetime import date
#from deep_translator import GoogleTranslator

#def _para_portugues(texto):
    #tradutor = GoogleTranslator(source= "en", target= "pt")
    #return tradutor.translate(texto)

def _remover_acentos(texto):
    nfkd = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in nfkd if not unicodedata.combining(c))

def normalizar_nome(nome):
    if not nome:
        return ""
    return nome.strip().title()

def normalizar_data(data):
    if not data:
        return None
    partes = data.strip().split("T")
    return partes[0]

def transformar_partida(partida):
    return {
        "data": normalizar_data(partida.get("data")),
        "equipe_casa": partida.get("equipe_casa"),
        "equipe_visitante": partida.get("equipe_visitante"),
        "gols_casa": partida.get("gols_casa"),
        "gols_fora": partida.get("gols_fora")
    }

def transformar_partidas(partidas):
    return [transformar_partida(partida) for partida in partidas]