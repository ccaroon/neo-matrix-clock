from SECRETS import DATA as secrets
from SETTINGS import DATA as settings

class Config:
    @classmethod
    def __get(cls, name, data, default=None):
        value = data

        parts = name.split(":")
        for part_name in parts:
            value = value.get(part_name, default)
            if value == default:
                break

        return value

    @classmethod
    def secret(cls, name, default=None):
        return cls.__get(name, secrets, default)

    @classmethod
    def setting(cls, name, default=None):
        return cls.__get(name, settings, default)
