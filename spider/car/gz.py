from lxml import etree
import requests


class GZ:

    def login(self):
        login_url = 'https://api.gzdata.com.cn/api/accounts/login'
        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Host": "api.gzdata.com.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.9.0"
        }
        data = '{"mobile":"18520225024","password":"8F8555F2A342F17F74B48A8C31ED9980","sha1Password":"EB61FA12DFFC2D400AB254F2F3FBBA83E78F4B04","appVersion":"2.1.6","systemVersion":"Android5.1.1"}'
        token = requests.post(url=login_url, headers=headers, data=data).json()["data"]
        digest_url = 'https://api.gzdata.com.cn/api/accounts/secret/apps/1000126'
        print(token)
        headers["token"] = token
        rs = requests.get(url=digest_url, headers=headers).json()
        # print(rs)
        cookie_url = 'http://202.98.194.97:8082/'
        params = {
            "code": "jdcwfcx",
            "ysgz_account_id": rs["data"]["data"],
            "ysgz_digest": rs["data"]["digest"],
            "ysgz_timestamp": rs["data"]["timestamp"],
        }
        headers["User-Agent"] = "Mozilla/5.0 (Linux; Android 5.1.1; SM-G955N Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36"

        cookie = requests.get(url=cookie_url, headers=headers, params=params)
        print(cookie.headers)
        # return cookie

    def get_data(self, info):

        cookie = self.login()
        # co_TokenId_url = 'http://h5.gzjjzd.gov.cn/Pages/Index.aspx?code=jdcwfcx&sign=04dcf17fcb97a2a648521f753cec4e66&time=1553146700094&userId=ysgz0401_user&deviceToken=88877878778'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
            "Cookie": cookie
        }
        # cookie = requests.get(url=co_TokenId_url,headers=headers,verify=False).headers.get("Set-Cookie")
        # print(cookie)

        url = 'http://h5.gzjjzd.gov.cn/Pages/violation/VioList.aspx'

        data = {
            "hphm": info["hphm"],
            "hpzl": info["hpzl"],
            "fdjh": info["fdjh"]
        }
        rs = requests.post(url=url, headers=headers, data=data)
        # print(rs.text)
        html = etree.HTML(rs.text)
        divs = html.xpath('//div[@class="card"]')
        # print(len(divs))

        result = {"code": 200, "msg": "成功！", "result": []}
        if len(divs):
            for x in divs:
                single = {}
                single["hphm"] = info["hphm"]
                single["hpzl"] = info.get("hpzl", '')
                single["cjh"] = info.get("cjh", '')
                single["fdjh"] = info.get("cjh", '')
                single["wfsj"] = x.xpath('div/div/text()')[1]
                single["wfdz"] = x.xpath('div/div/text()')[4]
                single["wfxw"] = x.xpath('div/div/text()')[7].split("-")[0]
                single["wfxwzt"] = x.xpath('div/div/text()')[7].split("-")[1]
                single["cjjgmc"] = x.xpath('div/div/text()')[10]
                clbj = x.xpath('div/div/text()')[13]
                if "未" in clbj:
                    single["clbj"] = 0
                    single["jkbj"] = 0
                elif "已" in clbj:
                    single["clbj"] = 1
                    single["jkbj"] = 1
                else:
                    single["clbj"] = 9
                    single["jkbj"] = 9
                result["result"].append(single)
            return result
        elif html.xpath('//div[@id="contentList"]/h3/span/text()'):
            print(html.xpath('//div[@id="contentList"]/h3/span/text()'))
            result["code"] = 200
            result["msg"] = html.xpath('//div[@id="contentList"]/h3/span/text()')[0]
            result["result"] = result
        else:
            result["code"] = 400
            result["msg"] = "车辆信息有误！"
            result["result"] = []
        return result


if __name__ == '__main__':
    p = GZ()
    # info = {"hpzl": "02", "hphm": "贵FZC209", "cjh": "179081", "fdjh": "520464"}
    info = {"hpzl": "02", "hphm": "贵CCW798", "cjh": "049765", "fdjh": "305696"}
    rs = p.get_data(info)
    print(rs)
