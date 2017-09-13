'''
存放对所有服务请求的函数
被monitor.py引用
'''
from passwords import *
import asyncio
import aiohttp
import json

async def plain_request(url = None, postdata = None, header = None):
    '''
    请求分类与中转.
    '''
    if url == None:
        return

    elif postdata == None :
        await plain_get(url, header)

    elif postdata is not None :
        await plain_post(url, postdata, header)

async def plain_get(url, header = None):
    '''
    plain_get:仅需url, header并直接发送请求的get请求
    '''
    if header is None:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                print(resp.status)
    else:
        async with aiohttp.ClientSession() as session:
            async with session.get(url = url, headers = header) as resp:
                print(resp.status)

async def plain_post(url, postdata, header = None):
    '''
    plain_post:仅需url, postdata, header并直接发送请求post请求
    '''
    if header is None:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json = postdata) as resp:
                print(resp.status)
    else:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json = postdata, headers = header) as resp:
                print(resp.status)

#-------------------------我是分割线-------------------------#

async def get_ele():
    '''
    查询电费API
    '''
    url = 'https://ccnubox.muxixyz.com/api/ele/'
    post_data = {
            "dor": "东1-101",
            "type": "air"
    }
    await plain_request(url, post_data)

async def get_apartments():
    '''
    部门信息
    '''
    url = "https://ccnubox.muxixyz.com/api/apartment/"
    await plain_request(url)

async def get_info():
    '''
    通知公告
    '''
    url = "https://ccnubox.muxixyz.com/api/webview_info/"
    await plain_request(url)

async def get_sites():
    '''
    常用网站
    '''
    url = "https://ccnubox.muxixyz.com/api/site/"
    await plain_request(url)

async def get_banners():
    '''
    获取Banner
    '''
    url = "https://ccnubox.muxixyz.com/api/banner/"
    await plain_request(url)

async def get_calendars():
    '''
    获取日历
    '''
    url = "https://ccnubox.muxixyz.com/api/calendar/"
    await plain_request(url)

async def get_ios_banner():
    '''
    IOS Banner
    '''
    url = "https://ccnubox.muxixyz.com/api/ios/banner/"
    await plain_request(url)

async def get_ios_calendars():
    '''
    IOS 日历
    '''
    url = "https://ccnubox.muxixyz.com/api/ios/calendar/"
    await plain_request(url)

async def get_start():
    '''
    获取闪屏
    '''
    url = "https://ccnubox.muxixyz.com/api/start/"
    await plain_request(url)

async def get_ios_add():
    '''
    IOS 推送用户注册
    '''
    url = "https://ccnubox.muxixyz.com/api/push/register"
    await plain_request(url, header = admin_header)

async def get_ios_push():
    '''
    IOS 推送
    '''
    url = "https://ccnubox.muxixyz.com/api/push/"
    await plain_request(url, header = admin_header)

async def main():
    '''
    调用其他所有函数
    用于测试
    '''
    await get_ele()
    await get_apartments()
    await get_info()
    await get_sites()
    await get_banners()
    await get_calendars()
    await get_ios_banner()
    await get_ios_calendars()
    await get_start()
    await get_ios_add()
    await get_ios_push()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())