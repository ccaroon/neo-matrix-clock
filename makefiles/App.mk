app-usage:
	@echo "Usage: 'include App.mk'"

install: boot.pyc main.pyc lib/secrets.py libs clocks lib/colors lib/glyphs

boot.pyc: boot.py
	touch boot.pyc
	make upload-as-boot FILE=boot.py

main.pyc: main.py
	touch main.pyc
	make upload-as-main FILE=main.py

# CLOCKS
clocks: clocks/__init__.pyc $(CLOCKS)

clocks/__init__.pyc: clocks/__init__.py
	touch $@
	ampy --port $(PORT) mkdir clocks
	make upload-file FILE=clocks/__init__.py

# LIBS
lib/secrets.py: .secrets
	./bin/gen_secrets.py

libs: lib/__init__.pyc $(LIBS)

lib/__init__.pyc: lib/__init__.py
	touch $@
	ampy --port $(PORT) mkdir lib
	make upload-file FILE=lib/__init__.py

# COLORS
lib/colors: lib/colors/__init__.pyc $(COLORS)

lib/colors/__init__.pyc: lib/colors/__init__.py
	touch $@
	ampy --port $(PORT) mkdir lib/colors
	make upload-file FILE=lib/colors/__init__.py

# GLYPHS
lib/glyphs: lib/glyphs/__init__.pyc $(GLYPHS)

lib/glyphs/__init__.pyc: lib/glyphs/__init__.py
	touch $@
	ampy --port $(PORT) mkdir lib/glyphs
	make upload-file FILE=lib/glyphs/__init__.py

%.pyc: %.py
	touch $@
	make upload-file FILE=$< $<

%.mpy: %.py
	mpy-cross $<
	make upload-file FILE=$@ $@

.PHONY: default install boot app libs clocks lib/colors
