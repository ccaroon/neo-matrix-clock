default:
	@echo "NeoPixel Matrix Clock(s)"
	@echo "---------------------------"
	@echo "-- Commands --"
	@echo "  * install - Install Code to Processor"
	@echo "  * shell - Micropython REPL on Device"
	@echo "  * clean - Clean Up"

include ./makefiles/Ports.mk
include ./makefiles/FileMgmt.mk

# NOTE: boot and main **must** be .py files ... not .mpy
BOOT = boot.pyc
APP  = main.pyc
LIBS = lib/adafruit_io.mpy lib/chronos.mpy lib/config.mpy lib/file_utils.mpy lib/glyph.mpy lib/neo_matrix.mpy lib/SECRETS.mpy lib/SETTINGS.mpy lib/wifi.mpy
COLORS = lib/colors/color_factory.mpy lib/colors/color.mpy lib/colors/holiday.mpy lib/colors/season.mpy
CLOCKS = clocks/clock.mpy clocks/binary.mpy clocks/digital.mpy clocks/fibonacci.mpy clocks/weather.mpy
GLYPHS = lib/glyphs/digit.mpy lib/glyphs/icon.mpy

# Order matters - This include must come after above vars are set.
include ./makefiles/App.mk

shell:
	picocom $(PORT) -b115200

clean:
	rm -f lib/SECRETS.py lib/SETTINGS.py
	find . -name "*.pyc" -exec rm -rf {} +
	find . -name "*.mpy" -exec rm -rf {} +
