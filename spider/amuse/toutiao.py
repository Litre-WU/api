import requests
from spider.tools.headers import async_ua


async def tt(info):
    url = 'http://lf.snssdk.com/api/news/feed/v47/'
    try:
        with requests.get(url=url, headers=await async_ua()) as rs:
            result = rs.json()
    except Exception as e:
        print(e)
        result = {
            "msg": "出错了！",
            "result": []
        }
    return result
