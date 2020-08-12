from random import randint
from datetime import datetime
import requests


class HA:

    async def get_data(self, info):
        headers = {

            "User-Agent": "Mozilla/5.0 (Linux; Android 4.4.2; SM-G955F Build/JLS36C) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36 MMWEBID/9941 MicroMessenger/6.7.3.1360(0x260703B3) NetType/WIFI Language/zh_CN Process/tools",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "app1.henanga.gov.cn",
            "X-Forwarded-For": str(randint(1, 255)) + '.' + str(randint(1, 255)) + '.' + str(
                randint(1, 255)) + '.' + str(randint(1, 255)),
        }
        t = str(datetime.now().now()).split(".")[0].replace(":", '').replace(" ", '').replace("-", '')
        # print(t)
        data = {"auth": '{"time_stamp":"%s"}' % t,
                "info": '{"HPHM":"%s","HPZL":"%s","CLSBDH":"%s","FZJG":"%s"}' % (
                info["hphm"][2:], info["hpzl"], info["cjh"], info["hphm"][:2])}

        with requests.get(url='http://124.172.189.180:5010/get/') as ip:
            proxies = {"http": ip.text}

        rs = requests.post(url='https://app1.henanga.gov.cn/jmth5/zzga/getJDCWZXX', headers=headers, data=data,
                           proxies=proxies)

        # print(rs.text)

        result = {"code": 200, "msg": "成功！", "result": []}
        try:
            if rs.json()["errCode"]:
                result["code"] = 400
                result["msg"] = rs.json()["msg"]
                return result

            else:

                for y in rs.json()["resultData"]:

                    single = {}
                    single["hphm"] = info["hphm"]
                    single["hpzl"] = info["hpzl"]
                    single["cjh"] = info["cjh"]
                    single["wfsj"] = y["wfsj"].split(".")[0]
                    single["wfxw"] = y["wfxwdm"]
                    single["wfdz"] = y["wfdz"]
                    single["wfjfs"] = y["wfjfs"]
                    single["wfxw"] = y["wfxwdm"]
                    single["wfxwzt"] = y["wfxw"]
                    single["fkje"] = y["fkje"]
                    if y["clbj"] == "未处理":
                        single["clbj"] = 0
                    else:
                        single["clbj"] = 1

                    result["result"].append(single)

                return result
        except Exception as e:
            print(e)
            return {"code": 500, "msg": "暂无法查询！"}


if __name__ == '__main__':
    # for x in range(10):
    p = HA()
    info = {"hpzl": "02", "hphm": "豫A7EE68", "cjh": "139464"}
    # info = {"hpzl": "02", "hphm": "豫E61D33", "cjh": "072806"}
    # info = {"hpzl": "02", "hphm": "豫CE755W", "cjh": "020774"}
    # info = {"hpzl": "02", "hphm": "豫R323RY", "cjh": "092386"}
    rs = p.get_data(info)
    print(rs)
