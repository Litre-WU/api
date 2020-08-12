import requests
from spider.tools.headers import ua
from random import randint
import time


async def adage_(info):
    url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php'
    params = {
        "from_mid": "1",
        "format": "json",
        "ie": "utf-8",
        "oe": "utf-8",
        "subtitle": "格言",
        "query": "格言",
        "rn": "8",
        "pn": str(randint(0, 95) * 8),
        "resource_id": "6844",
        "_": str(int(time.time() * 1000)),
    }
    headers = ua()

    try:
        with requests.get(url=url, params=params, headers=headers) as rs:
            data_list = []
            for a in rs.json()["data"][0]["disp_data"]:
                data = {
                    "adage": a["ename"],
                    "author": a["author"]
                }
                data_list.append(data)
            result = {
                "data": data_list
            }
    except Exception as e:
        print(e)
        result = {
            "msg": "不好意思,出错了！",
            "data": [{
                    "adage": "知识就是力量",
                    "author": "培根"
                }]
        }
    return result
