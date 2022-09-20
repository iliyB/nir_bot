import asyncio
from typing import Optional

from aiomysql import create_pool
from aiomysql.utils import _PoolContextManager

from nir_bot.bot.configs import db_settings


async def get_db_pool(db_name: str) -> Optional[_PoolContextManager]:
    try:
        return await create_pool(
            host=db_settings.DB_HOST,
            port=db_settings.DB_PORT,
            user=db_settings.DB_USER,
            passwords=db_settings.DB_PASSWORD,
            db=db_name,
            # loop=asyncio.get
        )
    except Exception as e:
        print(f"Not connected to database {db_name}:")
        print(f"Error: {e}:")
        return None
