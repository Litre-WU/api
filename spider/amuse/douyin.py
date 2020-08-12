import requests
from spider.tools.headers import ua


async def douyin(info):
    if info["type"] == None:
        url = 'https://aweme.snssdk.com/aweme/v1/hot/search/list/'
    if info["type"] == "hot":
        url = 'https://aweme.snssdk.com/aweme/v1/hot/search/list/'
    if info["type"] == "fascinating":
        count = info.get("count", "10")
        url = f'https://aweme.snssdk.com/aweme/v1/category/fascinating/list/?count={count}'
    if info["type"] == "music":
        url = 'https://api.amemv.com/aweme/v1/hotsearch/music/billboard/'
    if info["type"] == "video":
        url = "https://aweme.snssdk.com/aweme/v1/hotsearch/aweme/billboard/"
    if info["type"] == "energy":
        url = 'https://aweme.snssdk.com/aweme/v1/hotsearch/positive_energy/billboard/'
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