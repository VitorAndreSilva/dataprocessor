from datetime import date

def data_valida(texto):
    if not texto or texto is None:
        return False
    try:
        partes = texto.strip().split("T")
        date.fromisoformat(partes[0])
        return True
    except:
        print(texto)
        return False
    
def validar_equipe(texto):
    if not texto or not texto.strip():
        return False
    return True

def validar_gol(gol):
    if gol is None:
        return False
    return True

def validar_partida(partida):
    erros = []
    if not validar_equipe(partida.get("equipe_casa")):
        erros.append("Sem equipe 1")
    if not validar_equipe(partida.get("equipe_visitante")):
        erros.append("Sem equipe 2")
    if not validar_gol(partida.get("gols_casa")):
        erros.append("Sem gols")
    if not validar_gol(partida.get("gols_fora")):
        erros.append("Sem gols")
    if not data_valida(partida.get("data")):
        erros.append("Data inválida")
    return erros

def separar_registros(registros, funcao_validar, **kwargs):
    validos = []
    invalidos = []
    for registro in registros:
        erros = funcao_validar(registro, **kwargs)
        if erros:
            invalidos.append({"registro": registro, "erros": erros})
        else:
            validos.append(registro)
    return validos, invalidos