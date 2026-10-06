"""Transformação dos 21 landmarks do MediaPipe num vetor de características.

Normalizar é essencial: sem isto o modelo aprende ONDE está a mão no ecrã
(e a que distância da câmara) em vez de QUE FORMA tem a mão.
"""

import numpy as np

N_LANDMARKS = 21
WRIST = 0


def normalize_landmarks(points: np.ndarray) -> np.ndarray:
    """Recebe um array (21, 3) com x, y, z e devolve um vetor (63,).

    1. Translação: coordenadas relativas ao pulso (landmark 0).
    2. Escala: divide pela maior distância ao pulso, para ser independente
       do tamanho da mão e da distância à câmara.
    """
    pts = np.asarray(points, dtype=np.float32)
    if pts.shape != (N_LANDMARKS, 3):
        raise ValueError(f"Esperado array (21, 3), recebido {pts.shape}")

    rel = pts - pts[WRIST]
    scale = float(np.max(np.linalg.norm(rel, axis=1)))
    if scale < 1e-6:
        raise ValueError("Landmarks degenerados (todos no mesmo ponto)")

    return (rel / scale).reshape(-1)


def landmarks_to_array(hand_landmarks) -> np.ndarray:
    """Converte a lista de landmarks devolvida pelo HandLandmarker num array (21, 3)."""
    return np.array([[p.x, p.y, p.z] for p in hand_landmarks], dtype=np.float32)
