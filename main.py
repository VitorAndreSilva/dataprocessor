from leitor import carregar_partidas
from processador import media_gols
from validador import validar_partida, separar_registros
from transformador import transformar_partidas

# Carregar
partidas_raw = carregar_partidas("data/matches_original.csv")
# Validar
jogos_validos, jogos_invalidos = separar_registros(partidas_raw, validar_partida)
# Processar
media = media_gols(jogos_validos)
# Transformar
partidas = transformar_partidas(jogos_validos)

# Saída
print(f"jogos válidos: {len(jogos_validos)}")
print(f"jogos inválidos: {len(jogos_invalidos)}")
print(f"Média de gols: {media}")
print("Jogos:")
for jogo in partidas:
    print(jogo)