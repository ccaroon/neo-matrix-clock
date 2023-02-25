# -----------------------------------------------------------------------------
app-default:
	@echo "Usage: 'include App.mk'"

install: boot.pyc main.pyc secrets clocks libs

app-clean:
	make rm-file FILE=boot.py
	make rm-file FILE=main.py
	make rm-dir DIR=clocks
	make rm-dir DIR=lib

# BOOT & MAIN -----------------------------------------------------------------
# NOTE: boot and main **must** be .py files ... not .mpy
boot.pyc: boot.py
	touch boot.pyc
	make upload-as-boot FILE=boot.py

main.pyc: main.py
	touch main.pyc
	make upload-as-main FILE=main.py

# CLOCKS ----------------------------------------------------------------------
CLOCK_PY = $(shell find clocks -name "*.py")
CLOCK_MPY = $(CLOCK_PY:.py=.mpy)
CLOCK_PKG = $(shell find clocks -name __init__.py | sort --reverse)
CLOCK_PKG_MPY = $(CLOCK_PKG:.py=.mpy)
clocks: $(CLOCK_PKG_MPY) $(CLOCK_MPY)

# LIBS ------------------------------------------------------------------------
LIB_PY = $(shell find lib -name "*.py")
LIB_MPY = $(LIB_PY:.py=.mpy)
LIB_PKG = $(shell find lib -name __init__.py | sort --reverse)
LIB_PKG_MPY = $(LIB_PKG:.py=.mpy)
libs: $(LIB_PKG_MPY) $(LIB_MPY)

# GENERATED -------------------------------------------------------------------
GENERATED = lib/SECRETS.py lib/SETTINGS.py
secrets: $(GENERATED)

lib/SECRETS.py: .config/secrets
	./bin/gen_config_data.py

lib/SETTINGS.py: .config/settings
	./bin/gen_config_data.py

#------------------------------------------------------------------------------

%/__init__.mpy: %/__init__.py
	mpy-cross $<
	ampy --port $(PORT) mkdir $(shell dirname $@) --exists-okay

%.pyc: %.py
	touch $@
	make upload-file FILE=$< $<

%.mpy: %.py
	mpy-cross $<
	make upload-file FILE=$@ $@

.PHONY: app-default install libs clocks
