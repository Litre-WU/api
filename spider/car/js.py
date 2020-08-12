from tools.chaojiying import Chaojiying_Client
from lxml import etree
import requests
import tools.dict_match


class JS:

    async def get_data(self, info):
        try:
            return self.get_jsessionid(info)
        except Exception as e:
            print(e)
            return {"code": 500, "msg": "暂无法查询！"}

    def get_jsessionid(self,info):
        url = 'http://www.ezdrving.com/wxjswy/index.htm'
        headers = {
            "Host": "www.ezdrving.com",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.884.400 QQBrowser/9.0.2524.400",
        }
        rs = requests.post(url=url, headers=headers)
        jssionid = rs.headers.get("Set-Cookie").split(";")[0]
        # print(jssionid)
        meta = {"info":info,"jssionid":jssionid}
        return self.get_capture(meta)

    def get_capture(self, meta):
        url = 'http://www.ezdrving.com/wxjswy/portalLogin/verify.htm'
        headers = {
            "Cookie": meta["jssionid"] + ";"
        }
        rs = requests.get(url=url, headers=headers)
        # with open("yzm.jpeg", "wb+") as f:
        #     f.write(rs.content)

        cjy = Chaojiying_Client()
        # im = open('yzm.jpeg', 'rb').read()
        im = rs.content

        result = cjy.PostPic(im, 1902)

        if result.get("err_no") == -1005:

            print(result.get("err_str"))

            return result.get("err_str")

        else:

            yzm = result.get("pic_str")
            # yzm = input("请输入验证码:")
        meta["yzm"] = yzm
        return self.parse_data(meta)

    def parse_data(self, meta):

        url = 'http://www.ezdrving.com/wxjswy/illegal/doQueryOut.htm'

        data = f'plateType={meta["info"]["hpzl"]}&plateNO=%E8%8B%8F{meta["info"]["hphm"][1:]}&engineNO={meta["info"]["fdjh"]}&verify={meta["yzm"]}'

        headers = {
            "Host": "www.ezdrving.com",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
            "Cookie": meta["jssionid"]
        }
        try:
            rs = requests.post(url=url, headers=headers, data=data)
            # print(rs.text)
            html = etree.HTML(rs.text)
            trs = html.xpath('//table/tr')
            # print(len(trs))

            result = {"code": 200, "msg": "成功！", "result": []}

            for x in trs[1:]:
                single = {}
                single["hphm"] = meta["info"]["hphm"]
                single["hpzl"] = meta["info"]["hpzl"]
                single["fdjh"] = meta["info"]["fdjh"]
                single["cjh"] = meta["info"]["cjh"]
                single["xh"] = x.xpath('td/text()')[1]
                single["wfsj"] = x.xpath('td/text()')[-2]
                single["wfdz"] = x.xpath('td/text()')[3]
                single["wfxwzt"] = x.xpath('td/text()')[-4]

                xw2 = tools.dict_match.js(single["wfxwzt"])
                if xw2:
                    single["wfjfs"] = int(xw2.split("-")[0])
                    single["wfxw"] = xw2.split("-")[1]

                single["fkje"] = int(x.xpath('td/text()')[-1][:-1])

                result["result"].append(single)

            return result
        except Exception as e:
            print(e)
            return {"code": 500, "msg": "暂无法查询！"}


if __name__ == '__main__':
    p = JS()
    info = {"hphm": "苏H5011M", "hpzl": "02", "cjh": "HFFML6", "fdjh": "000716"}
    rs = p.get_data(info)
    print(rs)
