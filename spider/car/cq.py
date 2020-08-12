import requests
import json


class CQ:

    async def get_data(self, info):

        url = 'http://219.153.5.16:1808/cqjxj/admin/illegalprocess/waitillegalprocess'

        headers = {
            "Host": "219.153.5.16:1808",
            "Origin": "http://219.153.5.16:1808",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
            "Content-Type": "application/json",
            "Referer": "http://219.153.5.16:1808/"
        }
        with requests.get(url='http://124.172.189.180:5010/get/') as ip:
            proxies = {"http": ip.text}

        data = {"hphm": info["hphm"][1:], "hpzl": info["hpzl"], "clsbdh": info["fdjh"]}

        try:
            rs = requests.post(url=url, headers=headers, data=json.dumps(data), proxies=proxies).json()
            # print(rs)
            result = {"code": 200, "msg": "成功！", "result": []}

            if rs["status"]:

                for x in rs["data"]:
                    single = {}
                    single["hphm"] = info["hphm"]
                    single["hpzl"] = info["hpzl"]
                    single["fdjh"] = info["fdjh"]
                    single["cjh"] = info.get("cjh", "")
                    single["xh"] = x.get("xh", '')
                    single["wfsj"] = x.get("wfsj", '')
                    single["wfxw"] = x.get("wfxw", '')
                    single["wfxwzt"] = x.get("wfxwms", '')
                    single["fkje"] = int(x.get("fkje", ''))
                    single["wfjfs"] = int(x.get("wfjfs", ''))
                    single["wfdz"] = x.get("wfdz", '')
                    single["cjjgmc"] = x.get("cjjgmc", '')
                    clbj = x.get("clbj", '')
                    if "未" in clbj:
                        single["clbj"] = 0
                    elif "已" in clbj:
                        single["clbj"] = 1
                    else:
                        single["clbj"] = 9

                    result["result"].append(single)

                return result
            else:
                result["code"] = 400
                result["msg"] = rs["message"]
                return result
        except Exception as e:
            print(e)
            return {"code": 500, "msg": "暂无法查询！"}


if __name__ == '__main__':
    p = CQ()
    info = {"hphm": "渝AN385R", "fdjh": "757638", "hpzl": "02"}
    rs = p.get_data(info)
    print(rs)
