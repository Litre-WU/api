import requests
from spider.tools.headers import async_ua


async def zh(info):
    url = 'https://api.zhihu.com/topstory/hot-lists/total'
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
