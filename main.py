import argparse
import logging
from pathlib import Path

from dataprocessor.infra.fontes import fonte_a_partir_de_caminhos
from dataprocessor.infra.relatorios import criar_gerador
from dataprocessor.services.processamento import executar_processamento


def configurar_parser():
    parser = argparse.ArgumentParser(description="Processa partidas e times da Copa do Mundo 2026.")
    parser.add_argument("--partidas", required=True, help="Caminho do CSV de partidas.")
    parser.add_argument("--times", required=True, help="Caminho do CSV de times.")
    parser.add_argument("--config", required=True, help="Caminho do JSON de configuração.")
    parser.add_argument("--formato", choices=("texto", "json", "csv"), default="texto", help="Formato do relatório.")
    parser.add_argument("--output", type=Path, default=Path("output"), help="Pasta de saída.")
    return parser


def main(argv=None):
    args = configurar_parser().parse_args(argv)
    args.output.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=args.output / "dataprocessor.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    logging.info("Iniciando processamento")
    try:
        fonte = fonte_a_partir_de_caminhos(args.partidas, args.times, args.config)
        resultado = executar_processamento(fonte)
        relatorio = criar_gerador(args.formato).render(resultado)
        nome_arquivo = "relatorio.txt" if args.formato == "texto" else f"relatorio.{args.formato}"
        (args.output / nome_arquivo).write_text(relatorio, encoding="utf-8")
        logging.info(
            "Processamento concluído: %d partidas e %d equipes válidos",
            len(resultado.partidas),
            len(resultado.equipes),
        )
        print(relatorio, end="")
        return 0
    except (OSError, ValueError, KeyError) as erro:
        logging.exception("Falha no processamento")
        print(f"[ERRO] {erro}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
