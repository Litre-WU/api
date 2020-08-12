import requests
from tools.dict_match import sh as tr


class SH:

    def login(self):

        login_url = 'https://shanghaicity.openservice.kankanews.com/public/traffic/loginAPI'
        session = requests.Session()
        session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763"
        }
        data = {
            "username": "18520225024",
            "password": "a123456a"
        }
        rs = session.post(login_url, data=data)
        # print(rs.text)
        if rs.json()["error_code"] != 200:
            return self.login()
        else:
            return session

    def parse_data(self, info, session):
        url = 'https://shanghaicity.openservice.kankanews.com/public/traffic/jtwzapi'
        session.headers.update({"X-Requested-With": "XMLHttpRequest"})
        data = {
            "cardno": info["hphm"],
            "fdjh": info["fdjh"][-6:],
            "atype": info["hpzl"],
            "ctype": "wfqk",
            "remberme": "false"
        }
        rs = session.post(url=url, data=data)
        # print(rs.text)
        try:
            result = {"code": 200, "msg": "成功！", "result": []}
            if rs.json()["error_code"] == 200:

                for x in rs.json()["carinfo"]:
                    single = {}
                    single["hphm"] = info["hphm"]
                    single["hpzl"] = info["hpzl"]
                    single["fdjh"] = info.get("fdjh", "")
                    single["cjh"] = info.get("cjh", "")
                    single["wfsj"] = x.get("violatetime", "")
                    single["cjjg"] = x.get("cjjg", "")
                    single["wfdz"] = x.get("roadnum", "")
                    wfxwzt = x.get("wznr", "")
                    single["wfxwzt"] = wfxwzt
                    xw2fj = tr(wfxwzt)
                    if xw2fj:
                        single["fkje"] = xw2fj
                    else:
                        single["fkje"] = 200
                    wfxw = x.get("cfid", "")
                    single["wfxw"] = wfxw
                    if wfxw[1] == "7":
                        single["wfjfs"] = 12
                    else:
                        single["wfjfs"] = int(wfxw[1])
                    bj = x.get("clbj", "")
                    if "未处理" in bj:
                        single["clbj"] = 0
                    elif "已处理" in bj:
                        single["clbj"] = 1
                    if "未交款" in bj:
                        single["jkbj"] = 0
                    elif "已交款" in bj:
                        single["jkbj"] = 1
                    else:
                        single["clbj"] = single["jkbj"] = 9
                    result["result"].append(single)
            else:
                result = {"code": 400, "msg": rs.json()["error_message"]}

            return result

        except:

            return self.parse_data(info, session)

    def get_data(self, info):
        if info["hpzl"] == "52":
            return {"code": 400, "msg": "该车型尚无法查询！"}
        session = self.login()
        return self.parse_data(info, session)


if __name__ == '__main__':
    p = SH()
    # info = {'hphm': '沪BGH656', "hpzl": "02", 'cjh': '030091', 'fdjh': 'G2022938'}
    info = {'hphm': '沪AFR3990', "hpzl": "02", 'cjh': '006521', 'fdjh': '001234'}
    # p.login()
    rs = p.get_data(info)
    print(rs)
