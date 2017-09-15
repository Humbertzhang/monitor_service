import asyncio
from aiohttp import web
import aioredis
import pathlib
import json

#返回url:statuscode
async def server(loop):
    redis = await aioredis.create_redis(('localhost', 6379))
    keys = await redis.keys('*')
    dic = {}

    for key in keys:
        val = await redis.get(key)
        key = str(key).lstrip('b').strip("'")
        val = str(val).lstrip('b').strip("'")
        dic[str(key)] = str(val)

    redis.close()
    await redis.wait_closed()
    
    ret = web.json_response(dic)
    return ret

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = web.Application(loop = loop)
    app.router.add_get('/monitor', server)
    web.run_app(app,
                host = '127.0.0.1',
                port = 3001)