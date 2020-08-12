import requests


class SH:

    def login(self):

        login_url = 'https://api.eshimin.com/api/v5/account/basicInfo'
        headers = {
            "User-Agent": "OS/Android:8.0.0 Brand/HUAWEI:LND-AL30 Display/720*1360 EshiminApp/6.4.2",
            "CASTGC": "TGT-355098-toVqsRDnIdzlTZO4tWvNkwdssQPnCP73YPl5ykGCd9i6zcDQY7-cas01.example.org"
        }
        data = {
            "expire_time": "1556444543874",
            "data": "mG4Nsr3FrtkQdgmSR5tS6Y2ESKo3JaN0LqORV6ampRVVxZf8TtSg8yYvTcwfpnSzMzZjtToFEaUHS6HroqkYb53H6YQHg4lP8A0DsCaP/x/c5N1MEh6qdARW3YCpKFEDtKHX8vvmUWR7nWdVVGkR4FQObFuUKEV26DiN53B7MMc=",
            "content": "a5e474c94afa3259897c14fbda13a2fe54fc70a4861d8188d3ed7d2727a24a1b",
        }
        with requests.post(url=login_url, headers=headers, data=data) as res:
            pass
            # print(res.text)
        verify_url = 'https://my.eshimin.com/weizhang/electronbill/carBillIndex'
        headers["Cookie"] = "CASTGC=" + headers["CASTGC"]
        with requests.Session() as session:
            session.headers = headers
            with session.get(url=verify_url):
                return session

    async def get_data(self, info):

        if len(info["hphm"]) == 8:
            info["hpzl"] = 52
        params = {"account": info["hphm"], "fdjh": info["fdjh"], "hpzl": info["hpzl"]}

        session = self.login()
        url = 'https://my.eshimin.com/weizhang/electronbill/detail'

        with session.get(url=url, params=params) as rs:
            # print(rs.text)

            result = {"code": 200, "msg": "成功！", "result": []}

            if not rs.json().get("data"):
                result['code'] = 400
                result["msg"] = '车辆信息有误！'
                return result

            for x in rs.json().get("data"):

                single = {}
                single["hphm"] = info["hphm"]
                single["hpzl"] = info["hpzl"]
                single["cjh"] = info["cjh"]
                single["fdjh"] = info["fdjh"]
                if "-" in x["wfsj"]:
                    # single["wfsj"] = x["wfsj"].split(".")[0]
                    continue
                else:
                    time = []
                    for t in x["wfsj"]:
                        time.append(t)
                    single["wfsj"] = "".join(time[:4]) + '-' + "".join(time[4:6]) + '-' + "".join(
                        time[6:8]) + " " + "".join(time[8:10]) + ':' + "".join(time[10:12]) + ':00'
                single["wfxw"] = x.get("wfxw", "")
                single["wfdz"] = x.get("wfdz", "")
                single["fkje"] = int(x.get("fkje", ""))
                single["wfxwzt"] = x.get("xwsm", "")
                single["clbj"] = int(x.get("clbj", ""))
                single["xh"] = x.get("xh", "")
                single["wfjfs"] = x.get("kfsm", "")
                # single["jdsbh"] = x.get("tzsh", "")
                # single["jdsbh"] = x.get("jszh", "")

                result["result"].append(single)

            return result


if __name__ == '__main__':
    p = SH()
    # info = {"hpzl": "02", "hphm": "沪GF6980", "cjh": "450607", "fdjh": "012983"}
    # info = {"hpzl": "02", "hphm": "沪C7A1Z0", "cjh": "131390", "fdjh": "655058"}
    # info = {"hpzl": "02", "hphm": "沪A23T27", "cjh": "233976", "fdjh": "970862"}
    info = {"hpzl": "02", "hphm": "沪AFR3990", "cjh": "233976", "fdjh": "970862"}
    # info = {"hpzl": "52", "hphm": "沪AFF1122", "cjh": "", "fdjh": ""}
    # info = {"hpzl": "02", "hphm": "沪A12345", "cjh": "", "fdjh": ""}
    # info = {"hpzl": "52", "hphm": "沪C9H2G9", "cjh": "144064", "fdjh": "695757"}
    # info = {"hpzl": "02", "hphm": "沪C562UE", "cjh": "", "fdjh": ""}
    rs = p.get_data(info)
    print(rs)
    # p.login()
