#import os, csv
import os
from dataprocessor.services.processamento import executar_processamento
from dataprocessor.config import carregamento_configuracao_padrao
from dataprocessor.interfaces.menu import processar, exibir

def main():
    resultado = None
    formato_relatorio = 'texto'
    while True:
        print("\n=== DataProcessor Copa do Mundo 2026 - Menu ===/")
        print("1. Processar dados")
        print("2. Exibir relatório")
        print("3. Sair")
        opcao = input("Escolha uma opção: ").strip()
        os.system('clear')

        if opcao == "1":
            resultado = processar()
        elif opcao == "2":
            if resultado is None:
                print("Nenhum dado processado. Escolha a opção 1 para continuar")
                continue
            formato_relatorio = exibir(resultado, formato_relatorio)
        elif opcao == "3":
            break
        else:
            print("Opção inválida. Escolha entre as 3 opções disponíveis.")
            continue

    return 1
    '''
    app_config = carregamento_configuracao_padrao()
    resultado = executar_processamento(app_config)
    jogos_validos = resultado["jogos_validos"]
    jogos_invalidos = resultado["jogos_invalidos"]
    total_jogos = resultado["total_jogos"]
    media_gols = resultado["media_gols"]
    partidas = resultado["partidas"]
    total_equipes = resultado["total_equipes"]
    equipes = resultado["equipes"]

    # Saída
    print("===== DATAPROCESSOR - Copa do Mundo 2026 =====")
    print(f"jogos válidos: {len(jogos_validos)}/{len(total_jogos)}")
    print(f"jogos inválidos: {len(jogos_invalidos)}/{len(total_jogos)}")
    print(f"Média de gols: {media_gols}")
    print("Jogos:")
    for jogo in partidas:
        print(jogo)
    print("Equipes:")
    for equipe in equipes:
        print(equipe)
    print(f"Total de equipes: {total_equipes}")

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
    '''

if __name__ == "__main__":
    main()