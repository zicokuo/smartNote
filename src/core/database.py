from functools import wraps
from typing import Callable, Optional, T

from core.functions import log
from prisma_client import Prisma

db: Prisma = Prisma()


def db_this(f: Callable) -> Optional[Callable]:
    @wraps(f)
    async def wrapper(*args, **kwargs):
        await db.connect()
        try:
            return await f(db=db, *args, **kwargs)
        except BaseException as e:
            log.error(e)
            return e
        finally:
            await db.disconnect()

    return wrapper
