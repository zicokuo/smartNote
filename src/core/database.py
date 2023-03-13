from functools import wraps
from typing import Callable, Optional

from core.functions import log
from prisma_client import Prisma

db: Prisma = Prisma()


def db_this(f: Callable) -> Optional[Callable]:
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            db.disconnect()
            db.connect()
        finally:
            pass
        try:
            return f(db=db, *args, **kwargs)
        except BaseException as e:
            log.error(e)
            return e
        finally:
            db.disconnect()

    return wrapper
