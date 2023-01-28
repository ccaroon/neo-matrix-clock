#!/usr/bin/env python
import yaml
import pprint
# .secrets file should be formatted thusly
# ---------------------------------------
# secrets:
#   key1: value1
#   key2: value2
# ---------------------------------------
with open('.secrets', "r") as file:
    data = yaml.safe_load(file)

secrets = data.get('secrets', {})

with open("./lib/secrets.py", "w") as file:
    file.write(F"""
secrets = {pprint.pformat(secrets)}
""")
