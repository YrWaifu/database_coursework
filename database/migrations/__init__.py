import importlib

from settings import DB_CONFIG

migrations = [
    importlib.import_module("database.migrations.001_init"),
    importlib.import_module("database.migrations.002_fix3NF"),
    importlib.import_module("database.migrations.003_addUNIQ")
]

def up(n):
    if n > 0:
        migrations[n - 1].up(DB_CONFIG)
        return
    for m in migrations:
        print("Setting migration")
        m.up(DB_CONFIG)

def down():
    for m in migrations:
        print("Downgrading")
        m.down(DB_CONFIG)