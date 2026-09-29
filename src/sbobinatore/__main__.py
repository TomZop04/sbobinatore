import argparse
from pathlib import Path

from .transcriber import transcribe


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Trascrive un file audio localmente."
    )

    parser.add_argument(
        "audio",
        type=Path,
        help="File audio da trascrivere",
    )

    args = parser.parse_args()

    output = transcribe(args.audio)

    print()
    print(f"Trascrizione salvata in: {output}")


if __name__ == "__main__":
    main()
