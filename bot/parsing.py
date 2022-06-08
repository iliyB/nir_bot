import asyncio
import csv
import os
from typing import Dict, List

import aiofiles
from aiocsv import AsyncDictReader


async def wb_parse(number: str) -> Dict:
    dir_wb = os.path.join(os.getcwd(), "bd/wildberries_full")
    files = os.listdir(dir_wb)

    for file in files:
        file_path = os.path.join(dir_wb, file)
        print(file_path)
        async with aiofiles.open(file_path) as csv_file:
            async for row in AsyncDictReader(csv_file):
                if row.get("phone_number") == number:
                    return row

async def avito_parse(number: str) -> List[Dict]:
    dir_wb = os.path.join(os.getcwd(), "bd/avito_full")
    files = os.listdir(dir_wb)

    orders = []

    for file in files:
        file_path = os.path.join(dir_wb, file)
        print(file_path)
        async with aiofiles.open(file_path) as csv_file:
            async for row in AsyncDictReader(csv_file):
                if row.get("phone_number") == number:
                    orders.append(row)

    return orders

# asyncio.run(main())
