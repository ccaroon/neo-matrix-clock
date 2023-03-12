# CHANGELOG

## 2023-03-12
* Fixed DST bug in WeatherClock code that detects old data.
  - Basically needed to adjust last updated time for DST

## 2023-02-25
* Added Picasso BDay color set
* ColorFactory.get() can now recognize a hex color (`0xFFFFFF`)
* Added SecondsClock (just messin' around)
* Updated the `App.mk` Makefile to simplify it and make dependency mgmt better

## 2023-02-05
* Updated clock to be able to set the Holiday/Seasonal on-the-fly
  - i.e. does not require a restart to recogize the change

## 2023-01-28
* Added WeatherClock

## 2023-01-16
* Created Glyph class as a way to generically "draw" any type of alpha-num, etc.
* Implemented Digits (0-9) as Glyphs
* Implemented Emojis as Glyphs
* Added `draw_glyph()` method to NeoMatrix class
* Updated DigitalClock to use Glyph

## 2023-01-08
* NeoMatrix now works with RGB or RGBW LEDS
* Fixed AM/PM indicator bug in Digital clock
* Factored out Seasonal colors from ColorFactory
* Factored out Holiday colors from ColorFactory
* Moved all color related classes to `lib/colors` package

## 2023-01-07
* Updated `main.py` to change type of clock being displayed when the button on
  the NeoPixel Matrix is pressed. (Also had to wire the button to Pin #27 on the
  ESP32)
