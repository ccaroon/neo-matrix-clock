#!/usr/bin/env python
import yaml
import pprint

for name in ('settings','secrets'):
    print(f"Generating {name}...")
    data = {}

    with open(f".config/{name}", "r") as file:
        data = yaml.safe_load(file)

    with open(f"./lib/{name.upper()}.py", "w") as file:
        file.write(f"DATA = {pprint.pformat(data)}")
