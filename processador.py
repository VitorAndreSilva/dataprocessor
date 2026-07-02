def media_gols(partidas):
    gols_validos = []
    for partida in partidas:
        if partida["gols_casa"] is not None and partida["gols_fora"] is not None:
            gols_validos.append(partida["gols_casa"])
            gols_validos.append(partida["gols_fora"])
    if not gols_validos:
        print("Sem gols válidos")
        return 
    return round(sum(gols_validos) / len(gols_validos), 2)