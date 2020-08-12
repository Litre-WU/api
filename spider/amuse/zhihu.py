import requests
from spider.tools.headers import ua


async def zh(info):
    url = 'https://api.zhihu.com/topstory/hot-lists/total'
    try:
        header = ua()
        with requests.get(url=url, headers=header) as rs:
            result = rs.json()
    except Exception as e:
        print(e)
        result = {
            "msg": "出错了！",
            "result": []
        }
    return result
