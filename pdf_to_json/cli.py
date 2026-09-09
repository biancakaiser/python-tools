"""Command-line interface for PDF to JSON conversion."""

import argparse
import json
import sys
from pathlib import Path

from .extractor import extract_pdf


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract PDF metadata, form fields and text as JSON."
    )
    parser.add_argument("pdf", type=Path, help="Path to the PDF file")
    parser.add_argument(
        "-o", "--output", type=Path, help="Write JSON to this file instead of stdout"
    )
    parser.add_argument(
        "--pretty", action="store_true", help="Format JSON with indentation"
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        result = extract_pdf(args.pdf)
    except (OSError, ValueError) as error:
        print(f"Erro ao ler o PDF: {error}", file=sys.stderr)
        return 1

    serialized = json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None)
    if args.output:
        args.output.write_text(serialized + "\n", encoding="utf-8")
    else:
        print(serialized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())