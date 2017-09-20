'''
存放对所有服务请求的函数
被monitor.py引用
'''
from passwords import *
import asyncio
import aiohttp
import aioredis
import json
from random import randint

ROBOT_WEBHOOK = 'https://oapi.dingtalk.com/robot/send?access_token=5bb2fe9804da9d054f0637a822b4a943a1491157b91293540093111e970dc96b'

url_to_name = {
    "https://ccnubox.muxixyz.com/api/ele/":"电费查询",
    "https://ccnubox.muxixyz.com/api/apartment/":"部门信息",
    "https://ccnubox.muxixyz.com/api/webview_info/":"通知公告",
    "https://ccnubox.muxixyz.com/api/site/":"常用网站",
    "https://ccnubox.muxixyz.com/api/banner/":"Android获取Banner",
    "https://ccnubox.muxixyz.com/api/calendar/":"获取日历",
    "https://ccnubox.muxixyz.com/api/ios/calendar/":"IOS获取Banner",
    "https://ccnubox.muxixyz.com/api/start/":"获取闪屏",
    "https://ccnubox.muxixyz.com/api/push/register":"IOS推送用户注册",
    "https://ccnubox.muxixyz.com/api/push/":"IOS推送"
}

pictures = [
    "http://wx3.sinaimg.cn/mw690/6a2a7a61gy1fjlkhk7239g201o01odg8.gif",
    "http://wx1.sinaimg.cn/mw690/6a2a7a61gy1fjlki839edg201o01ogm1.gif",
    "http://wx3.sinaimg.cn/mw690/6a2a7a61gy1fjlki8nkkxg201o01odgb.gif",
    "http://wx4.sinaimg.cn/mw690/6a2a7a61gy1fjlkhkdl93g201e01edfv.gif",
    "http://wx2.sinaimg.cn/mw690/6a2a7a61gy1fjlkezjmfzg202z031jwn.gif",
    "http://wx2.sinaimg.cn/mw690/6a2a7a61gy1fjic3u0g29j202x03c0su.jpg",
    "http://wx2.sinaimg.cn/mw690/6a2a7a61gy1fjic3uj2xjj202g02s3yo.jpg",
    "http://wx3.sinaimg.cn/mw690/6a2a7a61ly1fjbf9n1c4xj202i02kwet.jpg",
    "https://b-ssl.duitang.com/uploads/item/201702/10/20170210165755_anZwz.thumb.700_0.jpeg",
    "https://b-ssl.duitang.com/uploads/item/201702/02/20170202203304_NamXA.thumb.700_0.jpeg",
]
async def robot_sender(url, old_status, new_status):
    if(old_status == 200 or old_status == 201):
        if(new_status != old_status and new_status != 200 and new_status != 201):
            picurl = "http://wx3.sinaimg.cn/mw690/6a2a7a61gy1fjlkhj49owg201o01o3zx.gif"
            txt = "![picture]({0})\n[{1}]API出现异常，状态码[{2}]".format(pictures[randint(0,9)], url_to_name[url], new_status)
            
            content = {
                "msgtype":"markdown",
                "markdown":{
                    "title":"华师匣子API监控警报",
                    "text": txt
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
