## ToDo
* [x] Test NeoPixel
* [x] Test RTC
* [x] Use WiFi/timeserver to set time on boot (lib/chronos.py)
* [x] Test with 8x5 NeoPixel matrix
* [x] Seal around JST wire solder points with liquid electrical tape
    - [x] 3 on matrix board
    - [x] 3 on processor board
* [ ] Check if wifi already connected during autoconnect
* [x] Update `make install` to include `clocks`
* [x] Colors class
  - [x] Basic colors
  - [x] Color groups (seasons, holidays, etc.)
* [ ] matrix freak-outs
  - too bright?
  - too many colors at one?
  - specific colors?
  - out of memory?
  - not enough power?

## Clocks
* [x] Binary
* [ ] Binary-coded sexagesimal
* [ ] Fibonacci
* [ ] Digital
  - [x] seconds "tick" up&down side pixels
  - [x] alternate showing hour & mins for X seconds at a time
  - colors: hour/min/both i.e. mix colors in digits to show hour&min at same time

## Features
* [ ] Bluetooth control

## Notes
* BLE Example: https://learn.adafruit.com/circuitpython-feather-ble-neopixel-hat
