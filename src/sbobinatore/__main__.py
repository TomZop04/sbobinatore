import argparse
from pathlib import Path

from .recorder import record
from .transcriber import transcribe


def main() -> None:
    parser = argparse.ArgumentParser(
            description="Registra e trascrive audio localmente."
            )

    parser.add_argument(
            "audio",
            type=Path,
            nargs="?",
            help="File audio da trascrivere. Se omesso, registra dal microfono.",
            )

    args = parser.parse_args()

    if args.audio is None:
        audio_file = record()
    else:
        audio_file = args.audio

    output = transcribe(audio_file)

    print()
    print(f"Trascrizione salvata in: {output}")


if __name__ == "__main__":
    main()
