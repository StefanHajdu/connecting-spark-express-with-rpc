import aiohttp
import asyncio
import time


URL = "http://localhost:4444/load"


async def load_data(session, id):
    async with session.post(
        url=URL,
        json={
            "id": f"002{id}",
            "df_path": "/home/stephenx/Documents/Datasets/domains_sub2.csv",
            "df_type": "csv",
        },
    ) as res:
        return await res.json()


async def load_data_0(session, id):
    async with session.post(
        url=URL,
        json={
            "id": f"001{id}",
            "df_path": "/home/stephenx/Documents/Datasets/domains_sub4.csv",
            "df_type": "csv",
        },
    ) as res:
        return await res.json()


async def main():
    session = aiohttp.ClientSession(headers={"Content-Type": "application/json"})
    requests_sub2 = [load_data(session, id) for id in range(1)]
    requests_sub3 = [load_data_0(session, id) for id in range(1)]
    responses_json = await asyncio.gather(*(requests_sub2 + requests_sub3))

    for r in responses_json:
        print()
        print(r)
        print()

    await session.close()


s = time.perf_counter()
asyncio.run(main())
print(f"total: {time.perf_counter() - s}")
