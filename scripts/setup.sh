#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$PROJECT_ROOT"

source scripts/versions.env

echo "==> Project root: $PROJECT_ROOT"
echo "==> whisper.cpp commit: $WHISPER_CPP_COMMIT"

# ------------------------------------------------------------
# Prerequisites
# ------------------------------------------------------------

for cmd in git python3 cmake; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
        echo "Errore: comando richiesto non trovato: $cmd" >&2
        exit 1
    fi
done

# ------------------------------------------------------------
# Python virtual environment
# ------------------------------------------------------------

if [[ ! -d ".venv" ]]; then
    echo "==> Creo ambiente virtuale Python..."
    python3 -m venv .venv
fi

echo "==> Installo sbobinatore nell'ambiente virtuale..."
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e .

# ------------------------------------------------------------
# whisper.cpp source
# ------------------------------------------------------------

WHISPER_DIR="$PROJECT_ROOT/vendor/whisper.cpp"

if [[ ! -d "$WHISPER_DIR/.git" ]]; then
    echo "==> Clono whisper.cpp..."
    mkdir -p "$PROJECT_ROOT/vendor"

    git clone "$WHISPER_CPP_REPO" "$WHISPER_DIR"
fi

cd "$WHISPER_DIR"

echo "==> Seleziono whisper.cpp al commit richiesto..."
git checkout --detach "$WHISPER_CPP_COMMIT"

cd "$PROJECT_ROOT"

# ------------------------------------------------------------
# Vulkan
# ------------------------------------------------------------

if ! command -v vulkaninfo >/dev/null 2>&1; then
    echo
    echo "Errore: vulkaninfo non trovato."
    echo "Installa Vulkan prima di eseguire nuovamente il setup."
    exit 1
fi

echo "==> GPU Vulkan disponibili:"
vulkaninfo --summary

# ------------------------------------------------------------
# Build whisper.cpp
# ------------------------------------------------------------

echo "==> Compilo whisper.cpp con Vulkan..."

cmake \
    -S "$WHISPER_DIR" \
    -B "$WHISPER_DIR/build" \
    -DGGML_VULKAN=ON

cmake \
    --build "$WHISPER_DIR/build" \
    --config Release \
    --parallel

# ------------------------------------------------------------
# Model
# ------------------------------------------------------------

MODEL_PATH="$PROJECT_ROOT/models/ggml-large-v3-turbo.bin"

mkdir -p "$PROJECT_ROOT/models"

if [[ ! -f "$MODEL_PATH" ]]; then
    echo "==> Scarico il modello large-v3-turbo..."

    bash "$WHISPER_DIR/models/download-ggml-model.sh" \
        large-v3-turbo \
        "$PROJECT_ROOT/models"
else
    echo "==> Modello già presente, salto il download."
fi

# ------------------------------------------------------------
# Final checks
# ------------------------------------------------------------

WHISPER_BIN="$WHISPER_DIR/build/bin/whisper-cli"

if [[ ! -x "$WHISPER_BIN" ]]; then
    echo "Errore: whisper-cli non trovato dopo la compilazione:" >&2
    echo "  $WHISPER_BIN" >&2
    exit 1
fi

if [[ ! -f "$MODEL_PATH" ]]; then
    echo "Errore: modello non trovato dopo il download:" >&2
    echo "  $MODEL_PATH" >&2
    exit 1
fi

echo
echo "========================================"
echo " Setup completato"
echo "========================================"
echo
echo "whisper-cli:"
echo "  $WHISPER_BIN"
echo
echo "modello:"
echo "  $MODEL_PATH"
echo
echo "Python:"
echo "  $PROJECT_ROOT/.venv/bin/python"
echo
echo "Per testare:"
echo "  $PROJECT_ROOT/.venv/bin/sbobinatore test.wav"
echo
