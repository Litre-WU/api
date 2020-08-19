import requests
from spider.tools.headers import async_ua


async def rs(info):
    url = 'https://api.weibo.cn/2/guest/page'
    params = {
        "containerid": "106003type=25&t=3&disable_hot=1&filter_type=realtimehot"
    }
    try:
        with requests.get(url=url, params=params, headers=await async_ua()) as rs:
            result = rs.json()
    except Exception as e:
        print(e)
        result = {
            "msg": "出错了！",
            "result": []
        }
    return result
