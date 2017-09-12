"""
用aiojobs控制请求.
发送请求给各个服务，获得状态码，存在Redis中．
Server部分从Redis中拿数据返回
"""
import asyncio
import aiohttp
import aioredis
import aiojobs
from passwords import b64_portalPass, b64_libPass, b64_admin

#Async Connect to redis
async def conn():
    '''
    与Redis建立连接
    '''
    conn = await aioredis.create_connection(
        ('localhost', 6379), encoding = 'utf-8'
    )

async funcs():
    pass

async def main():
    await conn()

    scheduler = aiojobs.create_scheduler()
    
    while True:
        scheduler.spawn(funcs())
        await asyncio.sleep(600.0)

    #先gracefuly关闭jobs的连接
    await scheduler.close()
    #再关闭与Redis的连接
    conn.close()
    await conn.wait_closed()

if __name__ == '__main__':
    main()