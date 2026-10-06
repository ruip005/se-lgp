// SE-LGP — Arduino Uno: interface física (LCD + botões) e protocolo série com o PC.
// Protocolo: ver docs/protocolo-serie.md
//
// Notas de memória (Uno tem só 2 KB de RAM):
//  - strings constantes com F("...") para ficarem na flash;
//  - buffers de tamanho fixo em vez da classe String (evita fragmentação).

#include <Arduino.h>
#include <Bounce2.h>
#include <LiquidCrystal_I2C.h>
#include <Wire.h>

// Endereço I2C do LCD: normalmente 0x27 ou 0x3F (confirmar com um I2C scanner)
constexpr uint8_t LCD_ADDR = 0x27;
constexpr uint8_t PIN_BTN_OK = 2;
constexpr uint8_t PIN_BTN_DEL = 3;
constexpr size_t LINE_MAX = 32;

LiquidCrystal_I2C lcd(LCD_ADDR, 16, 2);
Bounce2::Button btnOk;
Bounce2::Button btnDel;

char line[LINE_MAX + 1];
size_t lineLen = 0;
bool discarding = false;  // linha demasiado longa: ignorar até ao próximo '\n'

// Escreve uma linha completa no LCD (preenche o resto com espaços)
void printRow(uint8_t row, const char *text) {
  lcd.setCursor(0, row);
  uint8_t i = 0;
  for (; i < 16 && text[i] != '\0'; i++) lcd.write(text[i]);
  for (; i < 16; i++) lcd.write(' ');
}

void handleLine(const char *msg) {
  if (strcmp(msg, "PING") == 0) {
    Serial.println(F("PONG"));
  } else if (strncmp(msg, "L:", 2) == 0) {
    char buf[17];
    snprintf(buf, sizeof(buf), "Letra: %s", msg + 2);
    printRow(0, buf);
  } else if (strncmp(msg, "W:", 2) == 0) {
    printRow(1, msg + 2);
  } else {
    Serial.println(F("ERR:UNKNOWN"));
  }
}

void setup() {
  Serial.begin(115200);

  lcd.init();
  lcd.backlight();
  printRow(0, "SE-LGP");
  printRow(1, "A aguardar PC...");

  // INPUT_PULLUP: botão liga o pino ao GND, sem resistências externas
  btnOk.attach(PIN_BTN_OK, INPUT_PULLUP);
  btnOk.interval(25);
  btnOk.setPressedState(LOW);
  btnDel.attach(PIN_BTN_DEL, INPUT_PULLUP);
  btnDel.interval(25);
  btnDel.setPressedState(LOW);

  // O PC espera por isto antes de enviar (abrir a porta série reinicia o Uno)
  Serial.println(F("READY"));
}

void loop() {
  btnOk.update();
  btnDel.update();
  if (btnOk.pressed()) Serial.println(F("B:OK"));
  if (btnDel.pressed()) Serial.println(F("B:DEL"));

  while (Serial.available() > 0) {
    char c = static_cast<char>(Serial.read());
    if (c == '\r') continue;

    if (c == '\n') {
      if (!discarding && lineLen > 0) {
        line[lineLen] = '\0';
        handleLine(line);
      }
      lineLen = 0;
      discarding = false;
    } else if (discarding) {
      // ignorar o resto da linha longa
    } else if (lineLen < LINE_MAX) {
      line[lineLen++] = c;
    } else {
      discarding = true;
      lineLen = 0;
      Serial.println(F("ERR:OVERFLOW"));
    }
  }
}
