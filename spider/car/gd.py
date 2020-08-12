from random import randint
import requests
import json


class GD:

    def __init__(self):
        self.headers = {
            "content-type": "application/json",
            "User-Agent": f"Mozilla/5.0 (Linux; Android {str(randint(2,10))}.0; OPPO R11 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 MicroMessenger/7.0.1380(0x27000038) Process/appbrand0 NetType/WIFI Language/zh_CN",
            "X-Forwarded-For": str(randint(1, 255)) + '.' + str(randint(1, 255)) + '.' + str(
                randint(1, 255)) + '.' + str(randint(1, 255)),
        }

    async def get_data(self, info):

        data = {"hpzl": info["hpzl"], "hphm": info["hphm"].strip("粤"), "fdjh": info["fdjh"][-6:],
                "sjhm": "186" + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + str(
                    randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)), "code": "sxai",
                "thirdSessionId": f"wx_{str(randint(0, 255))}",
                }
        with requests.get(url='http://124.172.189.180:5010/get/') as ip:
            proxies = {"http": ip.text}

        try:
            result = requests.post(url='https://wxcity.xx-motor.com/gdjmt.wx.xcx/trafficSearch/vehicleIllegal.do',
                                   headers=self.headers, data=json.dumps(data), proxies=proxies)
            # print(self.result.text)
            if result.json()["code"] == -200:

                return result.json()

            elif result.json()["result"]["resList"][0]["plateNumber"]:

                rs = {"code": 200, "msg": "成功", "result": []}

                for x in result.json()["result"]["resList"]:
                    single = {}
                    single["hphm"] = info["hphm"]
                    single["hpzl"] = info["hpzl"]
                    single["fdjh"] = info["fdjh"]
                    single["cjh"] = info.get("cjh", '')
                    single["wfsj"] = x.get("violationTime", '')
                    single["wfdz"] = x.get("violationLocation", '')
                    single["wfxw"] = x.get("violationCode", '')
                    single["wfxwzt"] = x.get("violationBehavior", '')
                    single["wfjfs"] = int(x.get("violationPoints", ''))
                    single["fkje"] = int(x.get("fine", ''))
                    single["jdsbh"] = x.get("decisionNumber", '')
                    single["xh"] = x.get("notificationNumber", '')

                    rs["result"].append(single)

                return rs
                # return self.result.json()
            else:
                return {"code": 200, "msg": "没有违章！", "result": []}
        except Exception as e:
            print(e)
            return {"code": 500, "msg": "暂无法查询！"}


if __name__ == '__main__':
    p = GD()
    info = {"hpzl": "02", "hphm": "粤AC56Y9", "fdjh": "320847"}
    rs = p.get_date(info)
    print(rs)
