# from fake_useragent import UserAgent
from random import randint, choice
from tools.dict_match import ua
from tools.chaojiying import Chaojiying_Client
from tools.dict_match import sf2bh
import requests
import time


# import sys
#
# sys.setrecursionlimit(10000)
requests.adapters.DEFAULT_RETRIES = 3


class JZJF:

    def get_cookie(self, info):
        headers = {
            "Connection": "keep-alive",
            "User-Agent": ua(),
            "Referer": f'{info["protocol"]}://{info["city"]}.122.gov.cn/views/inquiry.html?q=j',
            # "X-Forwarded-For": str(randint(1, 255)) + '.' + str(randint(1, 255)) + '.' + str(
            #     randint(1, 255)) + '.' + str(randint(1, 255))
        }

        with requests.get(url='http://124.172.189.180:5010/get/') as ip:
            # print(ip.text)
            proxies = {"http": ip.text}
        # url = f'https://{info["city"]}.122.gov.cn/views/inquiry.html?q=j'
        url = f'{info["protocol"]}://{info["city"]}.122.gov.cn/user/m/index'

        with requests.Session() as session:
            session.headers = headers
            # print(proxies)
            if not int(info["doc"][:2]) in [34, 63]:
                session.proxies = proxies
            elif int(info["doc"][:2]) in [12, 21]:
                # session.keep_alive = False
                session.Origin = f'{info["protocol"]}://{info["city"]}.122.gov.cn'
                session.X_Requested_With = "XMLHttpRequest"
                # session.verify = False
            with session.get(url=url):
                return session

    def get_captcha(self, session, info):

        t = str(int(time.time() * 1000))
        with session.get(url=f'{info["protocol"]}://{info["city"]}.122.gov.cn/captcha?nocache={t}') as rs:
            if rs.text:
                # with open('yzm.jpeg', "wb+") as f:
                #     f.write(rs.content)
                cjy = Chaojiying_Client()
                im = rs.content
                result = cjy.PostPic(im, 1902)
                if result.get("err_no") == -1005:
                    print(result.get("err_str"))
                    return result.get("err_str")
                else:
                    yzm = result.get("pic_str")
                # print(yzm)
                # yzm = input("请输入验证码:")

                return yzm
            else:
                return self.get_captcha(session, info)

    async def get_data(self, info):

        dcity = [12, 21]
        # dcity = []

        if len(info["driver"]) != 18 or len(info["doc"]) != 12:
            return {"code": 400, "message": "驾驶证号码或驾驶证档案编号不正确！"}
        elif int(info["doc"][:2]) in dcity:
            return {"code": 400, "message": "该城市尚无法查询！"}

        elif sf2bh(int(info["doc"][:4])):
            info["city"] = sf2bh(int(info["doc"][:4]))
        else:
            info["city"] = sf2bh(int(info["doc"][:2]))
            if int(info["doc"][:2]) in [63, 12]:
                info["protocol"] = "http"
            elif info["doc"][:2] == "61":
                return {"code": 400, "message": "该城市尚无法查询！"}
            else:
                info["protocol"] = "https"

        session = self.get_cookie(info)
        yzm = self.get_captcha(session, info)
        url = f'{info["protocol"]}://{info["city"]}.122.gov.cn/m/publicquery/scores'
        data = {
            "jszh": info["driver"], "dabh": info["doc"], "captcha": yzm, "qm": "wf", "page": "1"
        }
        session.headers.update({"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"})
        with session.post(url=url, data=data) as rs:
            # print(rs.json())
            if rs.json()["code"] == 499:
                return await self.get_data(info)
            elif rs.json()["code"] == 200:
                return {"code": 200, "message": "成功", "score": int(rs.json()["data"]["ljjf"])}
            else:
                return {"code": rs.json()["code"], "message": rs.json()["message"]}


if __name__ == '__main__':
    p = JZJF()
    info = {"driver": "110222198607210030", "doc": "110007394744"}
    # info = {"driver": "330423195911021415", "doc": "330437103957"}
    # info = {"driver": "320322197206167617", "doc": "320300842533"}
    # info = {"driver": "320682199801063590", "doc": "320602748829"}
    # info = {"driver": "320722198612021214", "doc": "320700962782"}
    rs = p.get_data(info)
    print(rs)
