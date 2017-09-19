'''
存放对所有服务请求的函数
被monitor.py引用
'''
import emoji
from passwords import *
import asyncio
import aiohttp
import aioredis
import json


ROBOT_WEBHOOK = 'https://oapi.dingtalk.com/robot/send?access_token=5bb2fe9804da9d054f0637a822b4a943a1491157b91293540093111e970dc96b'

async def robot_sender(url, old_status, new_status):
    if(old_status == 200 or old_status == 201):
        if(new_status != old_status and new_status != 200 and new_status != 201):
            txt = "<华师匣子API监控警报😱>\n\nAPI : {0} \n\n状态 : {1}\n".format(url, new_status)
            txt = emoji.emojize(txt)
            content = {
                "msgtype":"text",
                "text":{
                    "content": txt
                }
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(ROBOT_WEBHOOK, json = content) as resp:
                    pass
async def plain_request(url = None, postdata = None, header = None,loop = None):
    '''
    请求分类与中转.
    '''
    if url == None:
        return

    elif postdata == None :
        await plain_get(url, header,loop = loop)

    elif postdata is not None :
        await plain_post(url, postdata, header,loop = loop)

async def plain_get(url, header = None, loop = None):
    '''
    plain_get:仅需url, header并直接发送请求的get请求
    '''
    if header is None:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                print(resp.status)
                
                redis = await aioredis.create_redis(
                    ('localhost', 6379), loop=loop )
                
                new_status = resp.status
                old_status = int(redis.get(url, resp.status))
                await robot_sender(url, old_status, new_status)

                await redis.set(url, resp.status)
                redis.close()
                await redis.wait_closed()
                

    else:
        async with aiohttp.ClientSession() as session:
            async with session.get(url = url, headers = header) as resp:
                print(resp.status)

                redis = await aioredis.create_redis(
                    ('localhost', 6379), loop=loop )
                
                new_status = resp.status
                old_status = int(redis.get(url, resp.status))
                await robot_sender(url, old_status, new_status)

                await redis.set(url, resp.status)
                redis.close()
                await redis.wait_closed()

async def plain_post(url, postdata, header = None,loop = None):
    '''
    plain_post:仅需url, postdata, header并直接发送请求post请求
    '''
    if header is None:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json = postdata) as resp:
                print(resp.status)

                redis = await aioredis.create_redis(
                    ('localhost', 6379), loop=loop )

                new_status = resp.status
                old_status = int(redis.get(url, resp.status))
                await robot_sender(url, old_status, new_status)
                
                await redis.set(url, resp.status)
                redis.close()
                await redis.wait_closed()

    else:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json = postdata, headers = header) as resp:
                print(resp.status)

                redis = await aioredis.create_redis(
                    ('localhost', 6379), loop=loop )

                new_status = resp.status
                old_status = int(redis.get(url, resp.status))
                await robot_sender(url, old_status, new_status)
                
                await redis.set(url, resp.status)
                redis.close()
                await redis.wait_closed()

#-------------------------我是分割线-------------------------#

async def get_ele(loop = None):
    '''
    查询电费API
    '''
    url = 'https://ccnubox.muxixyz.com/api/ele/'
    post_data = {
            "dor": "东1-101",
            "type": "air"
    }
    await plain_request(url, post_data, loop = loop)
    

async def get_apartments(loop = None):
    '''
    部门信息
    '''
    url = "https://ccnubox.muxixyz.com/api/apartment/"
    await plain_request(url, loop = loop)

async def get_info(loop = None):
    '''
    通知公告
    '''
    url = "https://ccnubox.muxixyz.com/api/webview_info/"
    await plain_request(url, loop = loop)

async def get_sites(loop = None):
    '''
    常用网站
    '''
    url = "https://ccnubox.muxixyz.com/api/site/"
    await plain_request(url, loop = loop)

async def get_banners(loop = None):
    '''
    获取Banner
    '''
    url = "https://ccnubox.muxixyz.com/api/banner/"
    await plain_request(url, loop = loop)

async def get_calendars(loop = None):
    '''
    获取日历
    '''
    url = "https://ccnubox.muxixyz.com/api/calendar/"
    await plain_request(url, loop = loop)

async def get_ios_banner(loop = None):
    '''
    IOS Banner
    '''
    url = "https://ccnubox.muxixyz.com/api/ios/banner/"
    await plain_request(url, loop = loop)

async def get_ios_calendars(loop = None):
    '''
    IOS 日历
    '''
    url = "https://ccnubox.muxixyz.com/api/ios/calendar/"
    await plain_request(url, loop = loop)

async def get_start(loop = None):
    '''
    获取闪屏
    '''
    url = "https://ccnubox.muxixyz.com/api/start/"
    await plain_request(url, loop = loop)

async def get_ios_add(loop = None):
    '''
    IOS 推送用户注册
    '''
    url = "https://ccnubox.muxixyz.com/api/push/register"
    await plain_request(url, header = admin_header, loop = loop)

async def get_ios_push(loop = None):
    '''
    IOS 推送
    '''
    url = "https://ccnubox.muxixyz.com/api/push/"
    await plain_request(url, header = admin_header, loop = loop)
