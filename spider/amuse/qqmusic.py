import requests
from spider.tools.headers import async_ua


async def qqmusic(info):
    topid = "4"
    count = "100"
    if info["topid"]:
        topid = info.get("topid", "4")
    if info["count"]:
        count = info.get("count", "100")
    url = 'http://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg'
    params = {
        "topid": topid,
        "song_begin": "0",
        "song_num": count,
    }
    try:
        with requests.get(url=url, params=params, headers=await async_ua()) as rs:
            result = rs.json()
    except Exception as e:
        print(e)
        result = {
            "msg": "出错了!",
            "result": []
        }
    info["result"] = result
    return result
