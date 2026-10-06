# SE-LGP · Leitura de Língua Gestual Portuguesa

Projeto da UC de **Sistemas Embebidos** (ESTGV · IPV, 2026/27). Uma câmara capta gestos da LGP, o MediaPipe extrai os pontos da mão, um classificador reconhece o gesto e um Arduino mostra o resultado num LCD.

Planeamento, requisitos e decisões (ADRs) estão no Notion do projeto.

## O que corre onde

| Componente | Onde corre | Porquê |
|---|---|---|
| Câmara + MediaPipe + classificador (`edge/`) | **No PC, sem Docker** | O Docker Desktop em Windows/macOS não dá acesso à webcam nem a portas USB/série |
| Firmware (`firmware/`) | Arduino Uno (PlatformIO) | Interface física: LCD + botões |
| Broker MQTT, PostgreSQL | Docker (opcional) | Só quando forem precisos (fase híbrida, métricas, histórico) |
| Testes / treino reprodutível | Docker (opcional) ou PC | Mesmo ambiente Linux para todos e para o CI |

## Arranque rápido (PC)

Requisitos: Git, [uv](https://docs.astral.sh/uv/), VS Code. Guia completo no Notion ("Guia de instalação do laboratório").

```bash
git clone <url-do-repo>
cd se-lgp
uv sync --group dev                     # cria .venv com Python 3.11 e as versões do uv.lock
uv run pre-commit install
cp .env.example .env                    # Windows (PowerShell): Copy-Item .env.example .env
uv run python scripts/download_model.py
uv run pytest
uv run python -m edge.smoke_test        # janela com a câmara e os 21 pontos da mão
```

> Nunca usar `pip install` dentro do projeto: `uv add <pacote>` e fazer commit do `uv.lock`.

## Serviços Docker (opcionais)

Requer Docker Desktop (Windows/macOS: com WSL2 / virtualização ativa na BIOS) ou Docker Engine (Linux).

```bash
docker compose --profile mqtt up -d       # Mosquitto em localhost:1883
docker compose --profile db up -d         # PostgreSQL em localhost:5432, Adminer em http://localhost:8081
docker compose --profile ml run --rm ml   # testes num Linux limpo
docker compose --profile mqtt --profile db down   # parar (acrescentar -v apaga os dados)
```

Para os clientes Python destes serviços: `uv sync --group dev --group services`.

## Arduino

```bash
cd firmware
pio run -t upload          # compilar e gravar
cd ..
uv run python -m edge.serial_ping   # requer LGP_SERIAL_PORT no .env
```

Protocolo e ligações: [`docs/protocolo-serie.md`](docs/protocolo-serie.md).

## Estrutura

```
edge/       captura, features, inferência, série (Python)
ml/         treino e avaliação
firmware/   projeto PlatformIO do Arduino Uno
docs/       protocolo série, arquitetura, relatório
docker/     configs dos serviços e Dockerfile de ML
scripts/    utilitários (download do modelo, ...)
tests/      testes pytest
data/       (fora do Git) CSVs de landmarks
models/     (fora do Git) modelos MediaPipe e treinados
```

## Convenções

- Commits: [Conventional Commits](https://www.conventionalcommits.org/) com o ID da tarefa do Notion: `feat(edge): suavização por votação [SE-6]`
- Um branch por tarefa (`se-6-suavizacao`), merge por Pull Request com o CI verde.
- Dataset, imagens, modelos e `.env` **nunca** vão para o Git (tamanho e RGPD).
