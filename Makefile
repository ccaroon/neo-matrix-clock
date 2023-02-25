default:
	@echo "NeoPixel Matrix Clock(s)"
	@echo "---------------------------"
	@echo "-- Commands --"
	@echo "  * install - Install Code to Processor"
	@echo "  * shell - Micropython REPL on Device"
	@echo "  * clean - Clean Up"

include ./makefiles/Ports.mk
include ./makefiles/FileMgmt.mk
include ./makefiles/App.mk

shell:
	picocom $(PORT) -b115200

clean:
	rm -f lib/SECRETS.py lib/SETTINGS.py
	find . -name "*.pyc" -exec rm -rf {} +
	find . -name "*.mpy" -exec rm -rf {} +
