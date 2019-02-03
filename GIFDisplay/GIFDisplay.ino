//#include <ESP8266WiFi.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SPITFT.h>
//#include "Adafruit_SPITFT_Macros.h"
#include <Adafruit_SSD1351.h>
#include <SPI.h>
#include "GIF.h"

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 128
#define NUM_PIXELS (SCREEN_WIDTH * SCREEN_HEIGHT)

#define SPI_SPEED 24000000

#define SCLK_PIN 14
#define MOSI_PIN 13
#define DC_PIN   5
#define CS_PIN   15
#define RST_PIN  4

//#define DC_PIN   33
//#define RST_PIN  32
//#define CS_PIN   15

Adafruit_SSD1351 tft = Adafruit_SSD1351(SCREEN_WIDTH, SCREEN_HEIGHT, &SPI, CS_PIN, DC_PIN, RST_PIN);

byte counter = 0;

uint32_t start = 0;
uint32_t end = 0;

uint16_t buf[NUM_PIXELS];

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  
  tft.begin();

  //WiFi.disconnect();
  //WiFi.forceSleepBegin();

  displayFrame(10);
  //displayFrame(0);
}

void loop() {
  // put your main code here, to run repeatedly:
  displayFrame(counter);
  
  counter++;
  if (counter == NUM_FRAMES) {
    counter = 0;
  }
  delay(DELAY);
}

void displayFrame(byte frame) {
  
  for (uint16_t i = 0; i < NUM_PIXELS; i++){
    byte index = pgm_read_byte_near(&frameData[frame][i]);
    buf[i] = pgm_read_word_near(&palette[index]);
  }
  
  tft.startWrite();

  tft.setAddrWindow(0, 0, 128, 128);
  
  for (uint16_t i = 0; i < NUM_PIXELS; i++){
    tft.write16(buf[i]);
  }
  
  tft.endWrite();
}
