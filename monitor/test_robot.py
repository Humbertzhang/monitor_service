from allfuncs import *

async def test_get():
    url = 'https://ccnubox.muxixyz.com/api/ele/'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            redis = await aioredis.create_redis(
                ('localhost', 6379), loop=loop )
            old = 200
            new = 404
            await robot_sender(url, old, new)
            redis.close()
            await redis.wait_closed()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_get())
    loop.close()
