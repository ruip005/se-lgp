"""Teste de fumo: câmara + MediaPipe Hand Landmarker (Tasks API).

Correr a partir da raiz do projeto:
    uv run python -m edge.smoke_test
"""

import time
from pathlib import Path

import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

from edge.camera import open_camera
from edge.config import get_settings


def main() -> None:
    cfg = get_settings()
    model = Path(cfg.model_path)
    if not model.exists():
        raise SystemExit(
            f"Modelo não encontrado em {model}. Corra: uv run python scripts/download_model.py"
        )

    options = vision.HandLandmarkerOptions(
        base_options=mp_python.BaseOptions(model_asset_path=str(model)),
        running_mode=vision.RunningMode.VIDEO,
        num_hands=1,
    )

    cap = open_camera(cfg.camera_index, cfg.camera_width, cfg.camera_height)
    t0 = time.perf_counter()
    last_ts = -1
    times: list[float] = []

    with vision.HandLandmarker.create_from_options(options) as landmarker:
        while True:
            ok, frame = cap.read()
            if not ok:
                print("Sem imagem da câmara")
                break

            # OpenCV entrega BGR; o MediaPipe espera RGB
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

            # No modo VIDEO o timestamp tem de ser estritamente crescente
            ts_ms = max(int((time.perf_counter() - t0) * 1000), last_ts + 1)
            last_ts = ts_ms

            start = time.perf_counter()
            result = landmarker.detect_for_video(image, ts_ms)
            ms = (time.perf_counter() - start) * 1000
            times.append(ms)

            h, w = frame.shape[:2]
            for hand in result.hand_landmarks:
                for p in hand:
                    cv2.circle(frame, (int(p.x * w), int(p.y * h)), 3, (0, 255, 0), -1)

            cv2.putText(
                frame, f"{ms:.0f} ms", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2
            )
            cv2.imshow("Smoke test - q para sair", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()

    if times:
        times.sort()
        p50 = times[len(times) // 2]
        p95 = times[int(len(times) * 0.95) - 1] if len(times) >= 20 else times[-1]
        print(f"Frames: {len(times)} | inferência p50: {p50:.1f} ms | p95: {p95:.1f} ms")
        print("Registem estes valores no Backlog (tarefa de captura) com o modelo do CPU.")


if __name__ == "__main__":
    main()
