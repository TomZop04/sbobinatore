from pathlib import Path
import subprocess

from .config import WHISPER_BIN, MODEL, LANGUAGE, TRANSCRIPTS_DIR


def transcribe(audio_file: Path) -> Path:
    audio_file = audio_file.resolve()
    output_dir = TRANSCRIPTS_DIR.resolve()

    if not WHISPER_BIN.exists():
        raise FileNotFoundError(f"whisper-cli non trovato: {WHISPER_BIN}")

    if not MODEL.exists():
        raise FileNotFoundError(f"modello non trovato: {MODEL}")

    if not audio_file.exists():
        raise FileNotFoundError(f"file audio non trovato: {audio_file}")

    output_dir.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [
            str(WHISPER_BIN),
            "-m",
            str(MODEL),
            "-f",
            str(audio_file),
            "-l",
            LANGUAGE,
            "-otxt",
            "-of",
            str(output_dir / audio_file.stem),
        ],
        check=True,
    )

    return output_dir / f"{audio_file.stem}.txt"
