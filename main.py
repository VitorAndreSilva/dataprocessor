from leitor import carregar_partidas, carregar_config
from processador import media_gols
from validador import validar_partida, separar_registros
from transformador import transformar_partidas
import os, csv

# Carregar
partidas_raw = carregar_partidas("data/matches_original.csv")
config = carregar_config("data/config.json")
# Validar
jogos_validos, jogos_invalidos = separar_registros(partidas_raw, validar_partida)
total_jogos = jogos_validos + jogos_invalidos
# Processar
media = media_gols(jogos_validos)
# Transformar
partidas = transformar_partidas(jogos_validos)

# Saída
print("===== DATAPROCESSOR - Copa do Mundo 2026 =====")
print(f"jogos válidos: {len(jogos_validos)}/{len(total_jogos)}")
print(f"jogos inválidos: {len(jogos_invalidos)}/{len(total_jogos)}")
print(f"Média de gols: {media}")
print("Jogos:")
for jogo in partidas:
    print(jogo)

os.makedirs("output", exist_ok=True)
caminho_arquivo = os.path.join("output", "partidas_processadas.csv")

if partidas:
    with open(caminho_arquivo, mode="w", encoding="utf-8") as arquivo_csv:
        cabecalho = partidas[0]         
        escritor = csv.DictWriter(arquivo_csv, fieldnames=cabecalho)
        escritor.writerows(partidas)
        
    print(f"\nArquivo salvo com sucesso em: {caminho_arquivo}")
else:
    print("\nNenhuma partida válida para salvar.")