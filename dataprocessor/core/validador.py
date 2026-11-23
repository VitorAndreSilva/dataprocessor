from datetime import date

from .resultados import RegistroInvalido


def data_valida(texto):
    if not texto:
        return False
    try:
        partes = texto.strip().split("T")
        date.fromisoformat(partes[0])
        return True
    except ValueError:
        return False


def validar_nome(texto):
    if not texto or not texto.strip():
        return False
    return True


def validar_gol(gol):
    if gol is None:
        return False
    return True


def validar_partida(partida):
    erros = []
    if not validar_nome(partida.equipe_casa):
        erros.append("Sem equipe 1")
    if not validar_nome(partida.equipe_fora):
        erros.append("Sem equipe 2")
    if not validar_gol(partida.gols_casa):
        erros.append("Sem gols")
    if not validar_gol(partida.gols_fora):
        erros.append("Sem gols")
    if not data_valida(partida.data):
        erros.append("Data inválida")
    return erros


def validar_equipe(equipe):
    erros = []
    if not validar_nome(equipe.nome):
        erros.append("Equipe sem nome")
    if not validar_nome(equipe.sigla):
        erros.append("Equipe sem sigla")
    return erros


def separar_registros(registros, funcao_validar, **kwargs):
    validos = []
    invalidos = []
    for registro in registros:
        erros = funcao_validar(registro, **kwargs)
        if erros:
            invalidos.append(RegistroInvalido(registro, tuple(erros)))
        else:
            validos.append(registro)
    return validos, invalidos
