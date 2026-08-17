import unicodedata
from datetime import date
from dataclasses import replace
#from deep_translator import GoogleTranslator

#def _para_portugues(texto):
    #tradutor = GoogleTranslator(source= "en", target= "pt")
    #try:
        #return tradutor.translate(texto)
    #except:
        #return texto

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
    return replace(
        partida,
        data=normalizar_data(partida.data),
        #equipe_casa=_para_portugues(partida.equipe_casa),
        #equipe_fora=_para_portugues(partida.equipe_fora),
        equipe_casa=partida.equipe_casa,
        equipe_fora=partida.equipe_fora,
        gols_casa=partida.gols_casa,
        gols_fora=partida.gols_fora
    )

def transformar_partidas(partidas):
    return [transformar_partida(partida) for partida in partidas]