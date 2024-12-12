import os
from . import prod
from . import dev


mode = os.getenv("MODE")

if mode == "dev":
    DB_CONFIG = prod.DB_CONFIG
    POOL_MIN_CONN = prod.POOL_MIN_CONN
    POOL_MAX_CONN = prod.POOL_MAX_CONN
else:
    DB_CONFIG = dev.DB_CONFIG
    POOL_MIN_CONN = dev.POOL_MIN_CONN
    POOL_MAX_CONN = dev.POOL_MAX_CONN