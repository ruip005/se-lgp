# Protocolo série PC ↔ Arduino

Texto ASCII, uma mensagem por linha terminada em `\n`, **115200 baud**. Linhas com mais de 32 caracteres são rejeitadas (`ERR:OVERFLOW`).

| Direção | Mensagem | Significado |
|---|---|---|
| PC → Arduino | `L:<letra>` | Letra candidata atual (linha 1 do LCD) |
| PC → Arduino | `W:<palavra>` | Palavra atual (linha 2 do LCD, máx. 16 caracteres visíveis) |
| PC → Arduino | `PING` | Teste de latência |
| Arduino → PC | `READY` | Enviado no arranque |
| Arduino → PC | `PONG` | Resposta a `PING` |
| Arduino → PC | `B:OK` | Botão confirmar pressionado |
| Arduino → PC | `B:DEL` | Botão apagar pressionado |
| Arduino → PC | `ERR:UNKNOWN` / `ERR:OVERFLOW` | Mensagem não reconhecida / demasiado longa |

## Regras

- Abrir a porta série **reinicia o Arduino Uno**. O PC só envia depois de receber `READY`.
- O LCD 16x2 só mostra ASCII: enviar palavras sem acentos (`Ligacao`, não `Ligação`).
- Só um programa pode ter a porta aberta: fechar o Serial Monitor antes de correr o Python.

## Ligações (Sprint 0)

| Componente | Pino Arduino |
|---|---|
| LCD I2C SDA | A4 |
| LCD I2C SCL | A5 |
| LCD VCC / GND | 5V / GND |
| Botão confirmar | D2 ↔ GND |
| Botão apagar | D3 ↔ GND |
