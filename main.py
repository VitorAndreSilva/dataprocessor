import os, csv
from dataprocessor.pipeline import executar_pipeline

def main():
    resultado = executar_pipeline("data/matches_original.csv", "data/config.json")
    jogos_validos = resultado["jogos_validos"]
    jogos_invalidos = resultado["jogos_invalidos"]
    total_jogos = resultado["total_jogos"]
    media_gols = resultado["media_gols"]
    partidas = resultado["partidas"]

    # Saída
    print("===== DATAPROCESSOR - Copa do Mundo 2026 =====")
    print(f"jogos válidos: {len(jogos_validos)}/{len(total_jogos)}")
    print(f"jogos inválidos: {len(jogos_invalidos)}/{len(total_jogos)}")
    print(f"Média de gols: {media_gols}")
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

if __name__ == "__main__":
    main()