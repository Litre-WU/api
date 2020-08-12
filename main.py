from fastapi import FastAPI, Header, Cookie
from typing import List
from pydantic import BaseModel
from starlette.requests import Request
from spider.amuse.sina import *
from spider.amuse.toutiao import *
from spider.amuse.zhihu import *
from spider.amuse.douban import *
from spider.amuse.movie import *
from spider.amuse.douyin import *
from spider.amuse.qqmusic import *
from spider.liter.adage import *
from spider.others.freeSMS import *
from tools.sf2o import trs
from spider.car.jzjf import JZJF
from spider.car.xcd import XCD
from spider.car.wzcx import Q

app = FastAPI()


# 测试

# class Item(BaseModel):
#     name: str
#     number: str

# @app.get("/item/{item_id}")
# async def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}
#
#
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}


# 首页
@app.get("/")
@app.post("/")
async def index(request: Request, x_token: List[str] = Header(None), user_agent: str = Header(None)):
    result = {
        "code": 200,
        "msg": "来了！老弟",
        "result": "你看这个面它又长又宽，就像这个碗它又大又圆",
        "info": {
            "ip": request.client.host,
            "X-Token": x_token,
            "UA": user_agent,
            "headers": request.headers.items()
        }
    }
    return result


# 娱乐类

# 微博热搜
@app.post('/sina/hot/')
@app.get('/sina/hot/')
async def hot_search(request: Request, x_token: List[str] = Header(None), user_agent: str = Header(None)):
    result = {
        "code": 200,
        "msg": "来了！老弟",
        "result": "你看这个面它又长又宽，就像这个碗它又大又圆",
        "info": {
            "ip": request.client.host,
            "X-Token": x_token,
            "UA": user_agent,
            "headers": request.headers.items()
        }
    }

    info = dict()
    try:
        result["result"] = await rs(info)
    except Exception as e:
        print(e)
        result["result"] = {
            "msg": "出错了！",
            "result": []
        }
    return result


# 今日头条
@app.get('/toutiao/hot/')
@app.post('/toutiao/hot/')
async def hot_tt(request: Request, x_token: List[str] = Header(None), user_agent: str = Header(None)):
    result = {
        "code": 200,
        "msg": "来了！老弟",
        "result": "你看这个面它又长又宽，就像这个碗它又大又圆",
        "info": {
            "ip": request.client.host,
            "X-Token": x_token,
            "UA": user_agent,
            "headers": request.headers.items()
        }
    }
    info = dict()
    try:
        result["result"] = await tt(info)
    except Exception as e:
        print(e)
        result["result"] = {
            "msg": "出错了！",
            "result": []
        }
    return result


# 知乎
@app.get('/zhihu/hot/')
@app.post('/zhihu/hot/')
async def hot_zhihu(request: Request, x_token: List[str] = Header(None), user_agent: str = Header(None)):
    result = {
        "code": 200,
        "msg": "来了！老弟",
        "result": "你看这个面它又长又宽，就像这个碗它又大又圆",
        "info": {
            "ip": request.client.host,
            "X-Token": x_token,
            "UA": user_agent,
            "headers": request.headers.items()
        }
    }
    info = dict()
    try:
        result["result"] = await zh(info)
    except Exception as e:
        print(e)
        result["result"] = {
            "msg": "出错了！",
            "result": []
        }
    return result


# 豆瓣

@app.get("/douban/hot/")
async def douban(request: Request, x_token: List[str] = Header(None), user_agent: str = Header(None),
                 type: str = "movie",
                 start: str = "0",
                 count: str = "50"):
    info = {"type": type, "start": start, "count": count}
    result = {
        "code": 200,
        "msg": "来了！老弟",
        "result": "你看这个面它又长又宽，就像这个碗它又大又圆",
        "info": {
            "ip": request.client.host,
            "X-Token": x_token,
            "UA": user_agent,
            "headers": request.headers.items()
        }
    }
    try:
        result["result"] = await douban_(info)
    except Exception as e:
        print(e)
        result["result"] = {
            "msg": "出错了！",
            "result": []
        }
    return result


class Douban(BaseModel):
    type: str = None
    start: str = None
    count: str = None


@app.post("/douban/hot/")
async def douban(data: Douban, request: Request, x_token: List[str] = Header(None), user_agent: str = Header(None)):
    info = data.dict()
    result = {
        "code": 200,
        "msg": "来了！老弟",
        "result": "你看这个面它又长又宽，就像这个碗它又大又圆",
        "info": {
            "ip": request.client.host,
            "X-Token": x_token,
            "UA": user_agent,
            "headers": request.headers.items()
        }
    }
    try:
        result["result"] = await douban_(info)
    except Exception as e:
        print(e)
        result["result"] = {
            "msg": "出错了！",
            "result": []
        }
    return result


@app.get("/douban/movie/hot/")
async def douban_movie(request: Request, x_token: List[str] = Header(None), user_agent: str = Header(None),
                       page: str = "1",
                       limit: str = "100"):
    info = {"page": page, "limit": limit}
    result = {
        "code": 200,
        "msg": "来了！老弟",
        "result": "你看这个面它又长又宽，就像这个碗它又大又圆",
        "info": {
            "ip": request.client.host,
            "X-Token": x_token,
            "UA": user_agent,
            "headers": request.headers.items()
        }
    }
    try:
        result["result"] = await db_hot(info)
    except Exception as e:
        print(e)
        result["result"] = {
            "msg": "出错了！",
            "result": []
        }
    return result


class Douban_Movie(BaseModel):
    page: str = None
    limit: str = None


@app.post("/douban/movie/hot/")
async def douban_movie(data: Douban_Movie, request: Request, x_token: List[str] = Header(None),
                       user_agent: str = Header(None)):
    info = data.dict()
    result = {
        "code": 200,
        "msg": "来了！老弟",
        "result": "你看这个面它又长又宽，就像这个碗它又大又圆",
        "info": {
            "ip": request.client.host,
            "X-Token": x_token,
            "UA": user_agent,
            "headers": request.headers.items()
        }
    }
    try:
        result["result"] = await db_hot(info)
    except Exception as e:
        print(e)
        result["result"] = {
            "msg": "出错了！",
            "result": []
        }
    return result


# 电影搜索

@app.get('/video/search/')
async def video_search(request: Request, x_token: List[str] = Header(None), user_agent: str = Header(None),
                       keyword: str = "绀青之拳"):
    info = {"keyword": keyword}
    result = {
        "code": 200,
        "msg": "来了！老弟",
        "result": "你看这个面它又长又宽，就像这个碗它又大又圆",
        "info": {
            "ip": request.client.host,
            "X-Token": x_token,
            "UA": user_agent,
            "headers": request.headers.items()
        }
    }
    try:
        # result["result"] = await search_movie(info)
        m = Movie()
        result["result"] = await m.run(info)
    except Exception as e:
        print(e)
        result["result"] = {
            "msg": "出错了！",
            "result": []
        }
    return result


class Video(BaseModel):
    keyword: str = "绀青之拳"


@app.post('/video/search/')
async def video_search(data: Video, request: Request, x_token: List[str] = Header(None),
                       user_agent: str = Header(None)):
    info = data.dict()
    result = {
        "code": 200,
        "msg": "来了！老弟",
        "result": "你看这个面它又长又宽，就像这个碗它又大又圆",
        "info": {
            "ip": request.client.host,
            "X-Token": x_token,
            "UA": user_agent,
            "headers": request.headers.items()
        }
    }
    try:
        # result["result"] = await search_movie(info)
        m = Movie()
        result["result"] = await m.run(info)
    except Exception as e:
        print(e)
        result["result"] = {
            "msg": "出错了！",
            "result": []
        }
    return result


# 抖音
class Douyin(BaseModel):
    type: str = "hot"
    count: str = "10"


@app.get("/douyin/")
async def dy(request: Request, x_token: List[str] = Header(None), user_agent: str = Header(None), type: str = "hot",
             count: str = "10"):
    info = {"type": type, "count": count}
    result = {
        "code": 200,
        "msg": "来了！老弟",
        "result": "你看这个面它又长又宽，就像这个碗它又大又圆",
        "info": {
            "ip": request.client.host,
            "X-Token": x_token,
            "UA": user_agent,
            "headers": request.headers.items()
        }
    }
    try:
        result["result"] = await douyin(info)
    except Exception as e:
        print(e)
        result["result"] = {
            "msg": "出错了！",
            "result": []
        }
    return result


@app.post("/douyin/")
async def dy(data: Douyin, request: Request, x_token: List[str] = Header(None), user_agent: str = Header(None)):
    info = data.dict()
    result = {
        "code": 200,
        "msg": "来了！老弟",
        "result": "你看这个面它又长又宽，就像这个碗它又大又圆",
        "info": {
            "ip": request.client.host,
            "X-Token": x_token,
            "UA": user_agent,
            "headers": request.headers.items()
        }
    }
    try:
        result["result"] = await douyin(info)
    except Exception as e:
        print(e)
        result["result"] = {
            "msg": "出错了！",
            "result": []
        }
    return result


# QQ音乐

@app.get("/qqmusic/")
async def music(request: Request, x_token: List[str] = Header(None), user_agent: str = Header(None), topid: str = "4",
                count: str = "100"):
    info = {"topid": topid, "count": count}
    result = {
        "code": 200,
        "msg": "来了！老弟",
        "result": "你看这个面它又长又宽，就像这个碗它又大又圆",
        "info": {
            "ip": request.client.host,
            "X-Token": x_token,
            "UA": user_agent,
            "headers": request.headers.items()
        }
    }
    try:
        result["result"] = await qqmusic(info)
    except Exception as e:
        print(e)
        result["result"] = {
            "msg": "出错了！",
            "result": []
        }
    return result


class QQMusic(BaseModel):
    topid: str = None
    count: str = None


@app.post("/qqmusic/")
async def music(data: QQMusic, request: Request, x_token: List[str] = Header(None), user_agent: str = Header(None)):
    info = data.dict()
    result = {
        "code": 200,
        "msg": "来了！老弟",
        "result": "你看这个面它又长又宽，就像这个碗它又大又圆",
        "info": {
            "ip": request.client.host,
            "X-Token": x_token,
            "UA": user_agent,
            "headers": request.headers.items()
        }
    }
    try:
        result["result"] = await qqmusic(info)
    except Exception as e:
        print(e)
        result["result"] = {
            "msg": "出错了！",
            "result": []
        }
    return result


# 文学类

# 格言
@app.get('/adage/')
@app.post('/adage/')
async def adage(request: Request, x_token: List[str] = Header(None), user_agent: str = Header(None)):
    info = dict()
    result = {
        "code": 200,
        "msg": "来了！老弟",
        "result": "你看这个面它又长又宽，就像这个碗它又大又圆",
        "info": {
            "ip": request.client.host,
            "X-Token": x_token,
            "UA": user_agent,
            "headers": request.headers.items()
        }
    }
    try:
        result["result"] = await adage_(info)
    except Exception as e:
        print(e)
        result["result"] = {
            "msg": "出错了！",
            "result": []
        }
    return result


# 工具类

# 免费手机号
@app.get("/sms/")
@app.post("/sms/")
async def phone(request: Request, x_token: List[str] = Header(None), user_agent: str = Header(None)):
    info = dict()
    result = {
        "code": 200,
        "msg": "来了！老弟",
        "result": "你看这个面它又长又宽，就像这个碗它又大又圆",
        "info": {
            "ip": request.client.host,
            "X-Token": x_token,
            "UA": user_agent,
            "headers": request.headers.items()
        }
    }
    try:
        result["result"] = await sms(info)
    except Exception as e:
        print(e)
        result["result"] = {
            "msg": "出错了！",
            "result": []
        }
    return result


# 短信内容

@app.get("/sms/msg/")
async def smsg(request: Request, x_token: List[str] = Header(None), user_agent: str = Header(None), phone: str = None):
    info = {"phone": phone}
    print(info)
    result = {
        "code": 200,
        "msg": "来了！老弟",
        "result": "你看这个面它又长又宽，就像这个碗它又大又圆",
        "info": {
            "ip": request.client.host,
            "X-Token": x_token,
            "UA": user_agent,
            "headers": request.headers.items()
        }
    }
    try:
        result["result"] = await msg(info)
    except Exception as e:
        print(e)
        result["result"] = {
            "msg": "出错了！",
            "result": []
        }
    return result


class Msg(BaseModel):
    phone: str = None


@app.post("/sms/msg/")
async def smsg(data: Msg, request: Request, x_token: List[str] = Header(None), user_agent: str = Header(None)):
    info = data.dict()
    result = {
        "code": 200,
        "msg": "来了！老弟",
        "result": "你看这个面它又长又宽，就像这个碗它又大又圆",
        "info": {
            "ip": request.client.host,
            "X-Token": x_token,
            "UA": user_agent,
            "headers": request.headers.items()
        }
    }
    try:
        result["result"] = await msg(info)
    except Exception as e:
        print(e)
        result["result"] = {
            "msg": "出错了！",
            "result": []
        }
    return result


# 车辆违章查询

class ApiData(BaseModel):
    hphm: str = "粤A*****"
    hpzl: str = "02"
    cjh: str = "123456"
    fdjh: str = "123456"


class JzData(BaseModel):
    driver: str = None
    doc: str = None


class XcdData(BaseModel):
    jdsbh: str = None


# @app.get("/api")
# async def api():
#     return {"code": 500, "msg": "维护中"}
#
#
# @app.post("/api")
# async def api():
#     return {"code": 500, "msg": "维护中"}
#

@app.get("/api")
async def cwz(request: Request, x_token: List[str] = Header(None), user_agent: str = Header(None),
              hphm: str = "粤A*****",
              hpzl: str = "02", cjh: str = "123456", fdjh: str = "123456"):
    info = {"hphm": hphm, "hpzl": hpzl, "cjh": cjh, "fdjh": fdjh}
    result = {
        "code": 200,
        "msg": "来了！老弟",
        "result": "你看这个面它又长又宽，就像这个碗它又大又圆",
        "info": {
            "ip": request.client.host,
            "X-Token": x_token,
            "UA": user_agent,
            "headers": request.headers.items()
        }
    }
    q = Q()
    try:
        result["result"] = await q.run(info)
        if result["result"]["code"] == 500:
            p = trs(info["hphm"][0])
            result["result"] = await p.get_data(info)
    except Exception as e:
        print(e)
        result["result"] = {"msg": "暂不支持查询"}
    return result


@app.post("/api")
async def cwz(data: ApiData, request: Request, x_token: List[str] = Header(None), user_agent: str = Header(None)):
    info = data.dict()
    result = {
        "code": 200,
        "msg": "来了！老弟",
        "result": "你看这个面它又长又宽，就像这个碗它又大又圆",
        "info": {
            "ip": request.client.host,
            "X-Token": x_token,
            "UA": user_agent,
            "headers": request.headers.items()
        }
    }
    q = Q()
    try:
        result["result"] = await q.run(info=info)
        if result["result"]["code"] == 500:
            p = trs(info["hphm"][0])
            result["result"] = await p.get_data(info)
    except Exception as e:
        print(e)
        result["result"] = {"msg": "暂不支持查询"}
    return result


@app.get("/jzjf")
async def jzjf(request: Request, x_token: List[str] = Header(None), user_agent: str = Header(None), driver: str = None,
               doc: str = None):
    info = {"driver": driver, "doc": doc}
    result = {
        "code": 200,
        "msg": "来了！老弟",
        "result": "你看这个面它又长又宽，就像这个碗它又大又圆",
        "info": {
            "ip": request.client.host,
            "X-Token": x_token,
            "UA": user_agent,
            "headers": request.headers.items()
        }
    }
    try:
        p = JZJF()
        result["result"] = await p.get_data(info=info)
    except Exception as e:
        print(e)
        result["result"] = {"message": "暂无法查询！"}
    return result


@app.post("/jzjf")
async def jsjf(data: JzData, request: Request, x_token: List[str] = Header(None), user_agent: str = Header(None)):
    info = data.dict()
    result = {
        "code": 200,
        "msg": "来了！老弟",
        "result": "你看这个面它又长又宽，就像这个碗它又大又圆",
        "info": {
            "ip": request.client.host,
            "X-Token": x_token,
            "UA": user_agent,
            "headers": request.headers.items()
        }
    }
    try:
        p = JZJF()
        result["result"] = await p.get_data(info=info)
    except Exception as e:
        print(e)
        result["result"] = {"message": "暂无法查询！"}
    return result


@app.get("/xcd")
async def xcd(request: Request, x_token: List[str] = Header(None), user_agent: str = Header(None), jdsbh: str = None):
    info = {"jdsbh": jdsbh}
    result = {
        "code": 200,
        "msg": "来了！老弟",
        "result": "你看这个面它又长又宽，就像这个碗它又大又圆",
        "info": {
            "ip": request.client.host,
            "X-Token": x_token,
            "UA": user_agent,
            "headers": request.headers.items()
        }
    }
    try:
        p = XCD()
        await p.action(info=info)
        result["result"] = info["result"]
    except Exception as e:
        print(e)
        result["result"] = {"msg": "暂无法查询！"}
    return result


@app.post("/xcd")
async def xcd(data: XcdData, request: Request, x_token: List[str] = Header(None), user_agent: str = Header(None)):
    info = data.dict()
    result = {
        "code": 200,
        "msg": "来了！老弟",
        "result": "你看这个面它又长又宽，就像这个碗它又大又圆",
        "info": {
            "ip": request.client.host,
            "X-Token": x_token,
            "UA": user_agent,
            "headers": request.headers.items()
        }
    }
    try:
        p = XCD()
        await p.action(info=info)
        result["result"] = info["result"]
    except Exception as e:
        result["result"] = {"msg": "暂无法查询！"}
    return result

