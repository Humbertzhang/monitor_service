#监控服务
监控服务由两个部分组成：
+ 发送请求并储存在redis中
+ 作为服务端从redis中拿数据并响应GET请求

URL: `localhost:3001/monitor`
METHOD:GET
RETURN DATA:

```
{
    "https://ccnubox.muxixyz.com/api/banner/": "200",
    "https://ccnubox.muxixyz.com/api/push/": "500",
    "https://ccnubox.muxixyz.com/api/start/": "200",
    "https://ccnubox.muxixyz.com/api/site/": "200",
    "https://ccnubox.muxixyz.com/api/apartment/": "200",
    "https://ccnubox.muxixyz.com/api/ele/": "200",
    "https://ccnubox.muxixyz.com/api/ios/calendar/": "404",
    "https://ccnubox.muxixyz.com/api/calendar/": "200",
    "https://ccnubox.muxixyz.com/api/push/register": "500",
    "https://ccnubox.muxixyz.com/api/ios/banner/": "200",
    "https://ccnubox.muxixyz.com/api/webview_info/": "200"
}

```
