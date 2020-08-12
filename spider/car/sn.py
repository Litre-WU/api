import requests


class SN:

    async def get_data(self, info):

        url = 'https://mobile.sxwinstar.net/wechat_access/api/v1/illegals/plateNumberSearch'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.884.400 QQBrowser/9.0.2524.400",
            "token_id": "1364ba8dd2cf453e8676b4690429e3d4"
        }
        params = {
            "plateNumber": info["hphm"],
            "engineNumber": info["fdjh"]
        }
        try:
            rs = requests.get(url=url, headers=headers, params=params).json()
            # print(rs)

            result = {"code": 200, "msg": "成功！", "result": []}
            if "semantic" in rs:
                result["code"] = 200
                result["msg"] = "无违章"
                result["result"] = result
                return result
            elif rs:
                for x in rs:
                    single = {}
                    single["hphm"] = info["hphm"]
                    single["hpzl"] = info["hpzl"]
                    single["fdjh"] = info.get("fdjh", "")
                    single["cjh"] = info.get("cjh", "")
                    single["xh"] = x.get("serialNumber", "")
                    single["wfsj"] = x.get("createdAtStr", "")
                    single["wfdz"] = x.get("place", "")
                    single["wfxw"] = x.get("actionCode", "")
                    single["wfxwzt"] = x.get("action", "")
                    single["wfjfs"] = int(x.get("dockPoints", ""))
                    single["fkje"] = int(x.get("penaltyAmount", ""))
                    single["clbj"] = x.get("status", "")
                    single["jkbj"] = x.get("status", "")

                    result["result"].append(single)

                return result
            else:
                result["code"] = 400
                result["msg"] = "查询失败"
                return result
        except Exception as e:
            print(e)
            return {"code": 500, "msg": "暂无法查询！"}


if __name__ == '__main__':

    p = SN()
    # info = {"hpzl": "02", "hphm": "陕A09VZ0", "cjh": "099135", "fdjh": "521239"}
    info = {"hpzl": "02", "hphm": "陕D62A89", "cjh": "798431", "fdjh": "010173"}
    # info = {"hpzl": "02", "hphm": "陕A1NG66", "cjh": "918231", "fdjh": "029005"}
    # info = {"hpzl": "02", "hphm": "陕A51CC0", "cjh": "083271", "fdjh": "739263"}
    # info = {"hpzl": "02", "hphm": "陕A2HH53", "cjh": "7169FA", "fdjh": "092564"}
    # info = {"hpzl": "02", "hphm": "陕BSF088", "cjh": "002461", "fdjh": "320398"}
    # info = {"hpzl": "02", "hphm": "陕A1T12V", "cjh": "M23983", "fdjh": "93D581"}
    # info = {"hpzl": "02", "hphm": "陕DLM429", "cjh": "015193", "fdjh": "001016"}
    rs = p.get_data(info)
    print(rs)
