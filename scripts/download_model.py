"""Descarrega o modelo pré-treinado do MediaPipe Hand Landmarker para models/.

    uv run python scripts/download_model.py
"""

import urllib.request
from pathlib import Path

# Se este link deixar de funcionar, procurar "Hand landmarks detection guide for Python"
# na documentação Google AI Edge e atualizar aqui.
URL = (
    "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
    "hand_landmarker/float16/latest/hand_landmarker.task"
)
DEST = Path("models/hand_landmarker.task")


def main() -> None:
    DEST.parent.mkdir(parents=True, exist_ok=True)
    if DEST.exists():
        print(f"Já existe: {DEST} ({DEST.stat().st_size / 1e6:.1f} MB)")
        return
    print(f"A descarregar {URL} ...")
    urllib.request.urlretrieve(URL, DEST)
    print(f"Guardado em {DEST} ({DEST.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
