import requests
from spider.tools.headers import ua


async def db_hot(info):
    page = "1"
    limit = "100"
    if info["page"]:
        page = info.get("page", "1")
    if info["limit"]:
        limit = info.get("limit", "100")
    url = "https://movie.douban.com/j/search_subjects"
    params = {
        "type": "movie",
        "tag": "热门",
        "sort": "recommend",
        "page_limit": limit,
        "page_start": int(page) - 1
    }

    try:
        with requests.get(url=url, params=params, headers=ua()) as rs:
            result = rs.json()
    except Exception as e:
        print(e)
        result = {
            "msg": "出错了！",
            "result": []
        }
    return result


async def douban_(info):
    start = "0"
    count = "50"
    if info["start"]:
        start = info.get("start", "0")
    if info["count"]:
        count = info.get("count", "100")
    if info["type"] == "book":
        url = 'https://frodo.douban.com/api/v2/subject_collection/book_top250/items'
    if info["type"] == "movie":
        url = 'https://frodo.douban.com/api/v2/subject_collection/movie_hot_gaia/items'
    if info["type"] == "music":
        url = 'https://frodo.douban.com/api/v2/subject_collection/music_single/items'
    if not info["type"]:
        url = 'https://frodo.douban.com/api/v2/subject_collection/movie_hot_gaia/items'
    params = {
        "start": start,
        "count": count,
    }
    headers = {
        "user-agent": "Rexxar-Core/0.1.3 api-client/1 com.douban.frodo/6.21.0(165) Android/28 product/MAR-AL00 vendor/HUAWEI model/MAR-AL00 rom/android network/wifi platform/mobile com.douban.frodo/6.21.0(165) Rexxar/1.2.151 platform/mobile 1.2.151",
    }
    try:
        with requests.get(url=url, params=params, headers=headers) as rs:
            result = rs.json()
    except Exception as e:
        print(e)
        result = {
            "msg": "出错了！",
            "result": []
        }
    return result
