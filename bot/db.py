import asyncio
from typing import Optional

from aiomysql import Pool, create_pool
from configs import db_settings


async def get_db_pool(db_name: str) -> Optional[Pool]:
    try:
        return await create_pool(
            host=db_settings.DB_HOST,
            port=db_settings.DB_PORT,
            user=db_settings.DB_USER,
            password=db_settings.DB_PASSWORD,
            db=db_name,
            # loop=asyncio.get
        )
    except Exception as e:
        print(f"Not connected to database {db_name}:")
        print(f"Error: {e}:")
        return None
