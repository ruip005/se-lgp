"""Teste de ligação ao Arduino: espera READY e mede a ida e volta com PING/PONG.

    uv run python -m edge.serial_ping
"""

import statistics
import time

import serial

from edge.config import get_settings

N_PINGS = 50


def wait_ready(port: serial.Serial, timeout_s: float = 5.0) -> None:
    # Abrir a porta série reinicia o Arduino Uno (linha DTR): esperar pelo READY
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        line = port.readline().decode(errors="ignore").strip()
        if line == "READY":
            return
    raise TimeoutError("O Arduino não enviou READY. Porta certa? Serial Monitor fechado?")


def main() -> None:
    cfg = get_settings()
    if not cfg.serial_port:
        raise SystemExit("Defina LGP_SERIAL_PORT no ficheiro .env")

    with serial.Serial(cfg.serial_port, cfg.serial_baud, timeout=1) as port:
        wait_ready(port)
        rtts = []
        for _ in range(N_PINGS):
            start = time.perf_counter()
            port.write(b"PING\n")
            reply = port.readline().decode(errors="ignore").strip()
            if reply == "PONG":
                rtts.append((time.perf_counter() - start) * 1000)

        if not rtts:
            raise SystemExit("Nenhum PONG recebido")
        print(
            f"{len(rtts)}/{N_PINGS} PONG | ida e volta média: {statistics.mean(rtts):.1f} ms "
            f"| máx: {max(rtts):.1f} ms"
        )
        port.write(b"L:-\nW:Ligacao OK\n")


if __name__ == "__main__":
    main()
