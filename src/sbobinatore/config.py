from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

WHISPER_BIN = PROJECT_ROOT / "vendor" / "whisper.cpp" / "build" / "bin" / "whisper-cli"
MODEL = PROJECT_ROOT / "models" / "ggml-large-v3-turbo.bin"

RECORDINGS_DIR = PROJECT_ROOT / "recordings"
TRANSCRIPTS_DIR = PROJECT_ROOT / "transcripts"

LANGUAGE = "it"
