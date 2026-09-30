from datetime import datetime
from pathlib import Path
import signal
import subprocess

from .config import RECORDINGS_DIR


def get_default_source() -> str:
    result = subprocess.run(
            ["wpctl", "status"],
            capture_output=True,
            text=True,
            check=True,
            )

    for line in result.stdout.splitlines():
        if "Audio/Source" in line:
            return line.split("Audio/Source", 1)[1].strip()

    raise RuntimeError("Nessuna sorgente audio predefinita trovata.")


def record() -> Path:
    RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = RECORDINGS_DIR / f"{timestamp}.wav"

    source = get_default_source()

    print(f"Sorgente audio: {source}")
    print("Registrazione in corso.")
    print("Premi Ctrl+C per fermare la registrazione.")

    process = subprocess.Popen(
            [
                "pw-record",
                "--target",
                source,
                str(output_file),
                ],
            )

    try:
        process.wait()
    except KeyboardInterrupt:
        print("\nFermo la registrazione...")
        process.send_signal(signal.SIGINT)
        process.wait()

    if process.returncode != 0:
        raise RuntimeError(
                f"pw-record è terminato con codice {process.returncode}."
                )

    if not output_file.exists():
        raise RuntimeError("La registrazione non ha prodotto alcun file audio.")

    print(f"Registrazione salvata in: {output_file}")

    return output_file
