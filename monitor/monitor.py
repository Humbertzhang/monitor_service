"""
发送请求给各个服务，获得状态码，存在Redis中．
Server部分从Redis中拿数据返回
"""
import asyncio
import aiohttp
import aioredis
from passwords import b64_portalPass, b64_libPass, b64_admin
from allfuncs import *


#Async Connect to redis
async def main(loop):
    '''
    调用各个发送请求的函数
    '''
    while True:
        await get_ele(loop)
        await get_apartments(loop)
        await get_info(loop)
        await get_sites(loop)
        await get_banners(loop)
        await get_calendars(loop)
        await get_ios_banner(loop)
        await get_ios_calendars(loop)
        await get_start(loop)
        await get_ios_add(loop)
        await get_ios_push(loop)
        await asyncio.sleep(600)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
