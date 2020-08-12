from random import randint
import requests


class HI:

    async def get_data(self, info):
        data = {"licensePlateType": info["hpzl"], "licensePlateNo": info["hphm"],
                "vehicleIdentifyNoLast4": info["cjh"][-4:]}

        url = 'https://service.gajj.haikou.gov.cn/illegal/vehicleIllegalQuery.do'
        headers = {'X-Forwarded-For': str(randint(1, 255)) + '.' + str(randint(1, 255)) + '.' + str(
            randint(1, 255)) + '.' + str(
            randint(1, 255))}
        with requests.get(url='http://124.172.189.180:5010/get/') as ip:
            # print(ip.text)
            proxies = {"http": ip.text}
        try:
            rs = requests.post(url=url, data=data, headers=headers, proxies=proxies)
            # print(rs.text)
            success = rs.json().get("success")

            result = {"code": 200, "msg": "成功！", "result": []}

            if success:
                self.result = rs.json()
                for x in rs.json().get("data"):
                    single = {}
                    single["hphm"] = info["hphm"]
                    single["hpzl"] = info["hpzl"]
                    single["fdjh"] = info["fdjh"]
                    single["cjh"] = info["cjh"]
                    single["wfsj"] = x.get("illegalTime")
                    single["wfdz"] = x.get("illegalAddr")
                    single["wfxw"] = x.get("illegalDesc")
                    if single["wfxw"]:
                        single["wfxw"] = x.get("illegalDesc").split("-")[0]
                        single["wfxwzt"] = x.get("illegalDesc").split("-")[1]
                    else:
                        single["wfxwzt"] = single["wfxw"]
                    single["fkje"] = x.get("punishAmt")
                    single["wfjfs"] = x.get("punishScore")
                    single["cjjgmc"] = x.get("agency")
                    jkbj = x.get("dealType")
                    if "NO" or "None" in jkbj:
                        single["jkbj"] = 0
                    else:
                        single["jkbj"] = 1
                    result["result"].append(single)

                return result
            elif "无未" in rs.json()["msg"]:
                result["msg"] = rs.json().get("msg")
                return result
            else:
                msg = rs.json().get("msg")
                result = {"code": 400, "msg": msg}
                return result
        except Exception as e:
            print(e)
            return {"code": 500, "msg": "暂无法查询！"}


if __name__ == '__main__':
    p = HI()
    # info = {"hpzl": "02", "hphm": "琼A0FC48", "cjh": "005662", "fdjh": "078881A"}
    info = {"hpzl": "02", "hphm": "琼AFR633", "cjh": "036051", "fdjh": "039479"}
    # info = {"hpzl": "02", "hphm": "琼BU5812", "cjh": "032728", "fdjh": "596425"}
    rs = p.get_data(info)
    print(rs)
