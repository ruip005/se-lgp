"""Abertura da câmara com o backend certo para cada sistema operativo."""

import sys

import cv2


def open_camera(index: int, width: int, height: int) -> cv2.VideoCapture:
    # CAP_DSHOW só existe no Windows (abre a câmara muito mais depressa que o MSMF).
    # Em Linux/macOS usar o backend por defeito, senão a câmara não abre.
    if sys.platform.startswith("win"):
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    else:
        cap = cv2.VideoCapture(index)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    if not cap.isOpened():
        raise RuntimeError(
            f"Não foi possível abrir a câmara {index}. Verifique permissões, "
            "se outra aplicação a está a usar, ou experimente outro LGP_CAMERA_INDEX."
        )
    return cap
