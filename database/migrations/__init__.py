import importlib

from settings import DB_CONFIG

migrations = [
    importlib.import_module("database.migrations.001_init")
]

def up(n):
    for m in migrations:
        print("Setting migration")
        m.up(DB_CONFIG)

def down():
    for m in migrations:
        print("Downgrading")
        m.down(DB_CONFIG)