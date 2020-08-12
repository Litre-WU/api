import requests
from tools.chaojiying import Chaojiying_Client
from lxml import etree


class SC:

    def __init__(self, *args, **kwargs):
        super(SC, self).__init__(*args, **kwargs)

    def login(self):

        index_url = 'https://jxtwap.cwddd.com/v1/index/index.html'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
        }
        cookie = requests.get(url=index_url, headers=headers).history[0].headers.get("Set-Cookie").split(";")[0]
        # print(cookie)
        headers["Cookie"] = cookie

        v_code = requests.get(url='http://cwapp.cwddd.com/v9.0/wap/public/verify', headers=headers)

        # with open("login.png", "wb+") as f:
        #     f.write(v_code.content)

        cjy = Chaojiying_Client()

        result = cjy.PostPic(v_code.content, 1902)

        if result.get("err_no") == -1005:

            print(result.get("err_str"))

            return result.get("err_str")

        else:

            yzm = result.get("pic_str")

        login_url = 'http://cwapp.cwddd.com/v9.0/wap/public/docache'
        headers["X-Requested-With"] = "XMLHttpRequest"

        data = {
            "username": "18520225024",
            "password": "a123456a",
            "verify": yzm,
        }
        logined = requests.post(url=login_url, headers=headers, data=data)
        # print(logined.text)
        if logined.json()["status"]:
            return cookie
        else:
            return self.login()

    async def get_data(self, info):
        cookie = self.login()
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Linux; Android 8.0.0; LND-AL30 Build/HONORLND-AL30; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36",
            "Cookie": cookie,
            "X-Requested-With": "com.cwddd.jxtmobile"
        }
        verify_code = requests.get(url='https://jxtwap.cwddd.com/v1/Public/verify', headers=headers)
        # with open("cw.png", "wb+") as f:
        #     f.write(verify_code.content)
        cjy = Chaojiying_Client()

        result = cjy.PostPic(verify_code.content, 1902)

        if result.get("err_no") == -1005:

            print(result.get("err_str"))

            return result.get("err_str")

        else:

            yzm = result.get("pic_str")
        # yzm = input("请输入验证码:")
        data = {
            "hpzl": info["hpzl"],
            "hphm": info["hphm"],
            "code": info["cjh"],
            "verify": yzm,
        }
        rs = requests.post(url='https://jxtwap.cwddd.com/v1/index/search.html', headers=headers, data=data)
        try:
            if not rs.json()["status"]:
                return await self.get_data(info)
        except Exception as e:

            html = etree.HTML(rs.text)
            divs = html.xpath('//div[@id="tab1"]/div')[:-1]
            # print(len(divs))

            rs = {"code": 200, "msg": "成功！", "result": []}
            for x in divs:
                single = {}
                # print(x.xpath('div/text()'))
                fkkf = x.xpath('div/text()')[0].strip()
                # print(fkkf)
                single["fkje"] = int(fkkf.split(" | ")[0].replace("罚款", "").replace("元", ""))
                single["wfjfs"] = int(fkkf.split(" | ")[1].replace("记", "").replace("分", ""))
                detail = x.xpath('div/p/text()')
                # print(detail)
                single["wfsj"] = detail[1]
                single["wfdz"] = detail[3]
                single["wfxwzt"] = detail[-1]
                rs["result"].append(single)

            return rs


if __name__ == '__main__':
    p = SC()
    # info = {"hpzl": "02", "hphm": "川A6W17H", "cjh": "038044"}
    info = {"hpzl": "02", "hphm": "川A0784Y", "cjh": "057625"}
    rs = p.get_data(info)
    print(rs)
