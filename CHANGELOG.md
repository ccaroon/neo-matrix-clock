# CHANGELOG

## 2023-01-08
* NeoMatrix now works with RGB or RGBW LEDS
* Fixed AM/PM indicator bug in Digital clock
* Factored out Seasonal colors from ColorFactory
* Moved all color related classes to `lib/colors` package

## 2023-01-07
* Updated `main.py` to change type of clock being displayed when the button on
  the NeoPixel Matrix is pressed. (Also had to wire the button to Pin #27 on the
  ESP32)
