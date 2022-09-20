import asyncio
from typing import Dict, Optional

from aiomysql import Pool, create_pool
from configs import db_settings
from py_singleton import singleton


class CreatePoolException(Exception):
    pass


@singleton
class DBPoolManager:
    pools: Dict[str, Pool] = {}

    async def get_connect(self, db_name: str) -> Pool:
        if db_name in self.pools:
            print(f"Get connect to {db_name}")
            return self.pools[db_name]

        try:
            new_pool = await self._create_db_pool(db_name)
            self.pools[db_name] = new_pool
            print(f"Create connect to {db_name}")
            return new_pool
        except Exception as e:
            print(f"Not connected to database {db_name}:")
            print(f"Error: {e}:")
            raise CreatePoolException

    @staticmethod
    async def _create_db_pool(db_name: str) -> Optional[Pool]:
        return await create_pool(
            host=db_settings.DB_HOST,
            port=db_settings.DB_PORT,
            user=db_settings.DB_USER,
            password=db_settings.DB_PASSWORD,
            db=db_name,
        )
