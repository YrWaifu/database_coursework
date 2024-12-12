import importlib

from settings import DB_CONFIG

migrations = [
    importlib.import_module("database.migrations.001_init")
]

def up(n):
    for m in migrations:
        m.up(DB_CONFIG)
#
# def down():
