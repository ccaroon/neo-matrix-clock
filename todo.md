## ToDo
* [x] Test NeoPixel
* [x] Test RTC
* [x] Use WiFi/timeserver to set time on boot (lib/chronos.py)
* [x] Test with 8x5 NeoPixel matrix
* [x] Seal around JST wire solder points with liquid electrical tape
    - [x] 3 on matrix board
    - [x] 3 on processor board
* [x] Check if wifi already connected during autoconnect
* [x] Update `make install` to include `clocks`
* [x] Colors class
  - [x] Basic colors
  - [x] Color groups (seasons, holidays, etc.)
* [x] matrix freak-outs
  > Before connecting a NeoPixel strip to ANY source of power, a large capacitor (500–1000 µF at 6.3 Volts or higher) across the + and – terminals provides a small power reservoir for abrupt changes in brightness that the power source might not otherwise handle — a common source of NeoPixel “glitching.”
  - too bright?
  - too many colors at one?
  - specific colors?
  - out of memory?
  - not enough power?
  - Solution: Had a "bad" pixel on the RGBW NeoPixel Matrix
* [x] Add more seasons/holidays colors
  - [x] Factor out Season from ColorFactory
  - [x] Factor out Holidays from ColorFactory
* [M] Better way to mkdirs and install files (Makefile)
* [x] Glyphs lib to draw chars & digits
  - [x] Refactory DigitalClock to use
* [-] General code cleanup
* [M] Update clock code to be able to change colors on-the-fly (for season & holidays)
* [x] Move this list to a Trello project

## Clocks
* [x] Binary
* [M] Binary-coded sexagesimal
* [x] Fibonacci
* [x] Digital
  - [x] seconds "tick" up&down side pixels
  - [x] alternate showing hour & mins for X seconds at a time
  - [?] colors: hour/min/both i.e. mix colors in digits to show hour&min at same time
* [M] Countdown in Days
* [M] Morse Code

## Features
* [M] Bluetooth control

## Notes
* BLE Example: https://learn.adafruit.com/circuitpython-feather-ble-neopixel-hat
