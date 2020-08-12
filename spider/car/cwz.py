from random import randint, choice
import requests


class CWZ:

    async def get_data(self, info):
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 4.4.2; SM-G955F Build/JLS36C) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36",
            'X-Forwarded-For': str(randint(1, 255)) + '.' + str(randint(1, 255)) + '.' + str(
                randint(1, 255)) + '.' + str(
                randint(1, 255)),
        }

        with requests.get(url='http://124.172.189.180:5010/get/') as ip:
            # print(ip.text)
            proxies = {"http": ip.text}
        data = {
            "hpzl": info["hpzl"],
            "hphm": info["hphm"],
            "engine": info["fdjh"],
            "body": info["cjh"],
            "source": "ws",
        }
        try:
            rs = requests.post(url='https://sp0.baidu.com/5LMDcjW6BwF3otqbppnN2DJv/traffic.pae.baidu.com/data/query',
                               headers=headers, data=data, proxies=proxies)
            # print(rs.text)

            result = {"code": 200, "msg": "成功！", "result": []}

            if rs.json()["status"] == -22:

                result["code"] = 400
                result["msg"] = rs.json()["msg"]

                return result

            elif rs.json()["status"] == -200:

                result["msg"] = rs.json()["msg"]
                return result

            elif rs.json()["status"] == 0:

                for x in rs.json()["data"]["lists"]:
                    single = {}
                    single["hphm"] = info["hphm"]
                    single["hpzl"] = info["hpzl"]
                    single["cjh"] = info["cjh"]
                    single["fdjh"] = info["fdjh"]
                    single["xh"] = x.get("item_id", '')
                    single["wfsj"] = x.get("time", '')
                    single["wfxwzt"] = x.get("violation_type", '')
                    single["fkje"] = x.get("fine", '')
                    single["wfjfs"] = x.get("point", '')
                    single["wfdz"] = x.get("address", '')
                    single["wfcs"] = x.get("city_code", '')

                    result["result"].append(single)

                return result

            else:
                result["code"] = 400
                result["msg"] = rs.json()["msg"]
                return result
        except Exception as e:
            print(e)
            return {"code": 500, "msg": "暂无法查询！"}


if __name__ == '__main__':
    p = CWZ()
    info = {"hpzl": "02", "hphm": "豫A7EE68", "cjh": "139464", "fdjh": "643001"}
    # info = {"hpzl": "02", "hphm": "湘MEU927", "cjh": "007234", "fdjh": "204891"}
    rs = p.get_data(info)
    print(rs)
