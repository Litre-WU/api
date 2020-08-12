import requests
from lxml import etree


class SD:

    async def get_data(self, info):
        sign_url = 'http://sms.czfw.cn/tpfwh/Service/HandServer.ashx?Method=checkwfcx'
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "http://sms.czfw.cn",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.884.400 QQBrowser/9.0.2524.400",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "http://sms.czfw.cn/tpfwh/wzz/queryvio.aspx?ts=1556262833&sign=44BA02E3DAA53403A55E39B2F48D9523"
        }
        data = {
            "hphm": info["hphm"],
            "hpzl": info["hpzl"],
            "fdjh": info["fdjh"][-4:],
            "openId": "o6wm-jg0nu03zj4QhItDAg-GQuKg",
        }
        sign = requests.post(url=sign_url, headers=headers, data=data, verify=False)
        # print(sign.text)

        data_url = 'http://sms.czfw.cn/tpfwh/wzz/wfxx.aspx'
        headers["Cookie"] = "tpfwhopenId=o6wm-jg0nu03zj4QhItDAg-GQuKg"
        data = {
            "hphm": info["hphm"],
            "hpzl": info["hpzl"],
            "fdjh": info["fdjh"][-4:],
            "ts": sign.json()["ts"],
            "sign": sign.json()["sign"],
        }
        try:
            rs = requests.post(url=data_url, headers=headers, data=data, verify=False)
            # print(rs.text)
            html = etree.HTML(rs.text)
            total = html.xpath('//article/div[@class="art-btm"]/span[@class="Arial"]/text()')[0]
            # print(total)
            result = {"code": 200, "msg": "成功！", "result": []}
            if int(total):
                lis = html.xpath('//div[@class="main"]/ul/li')

                for x in lis:
                    single = {}
                    single["wfdz"] = x.xpath('div[@class="cbp_tmlabel"]/text()')[0]
                    single["wfxwzt"] = x.xpath('div[@class="cbp_tmlabel"]/p[@class="cont"]/text()')[0].split("，")[0]
                    single["fkje"] = int(x.xpath('div[@class="cbp_tmlabel"]/p[@class="cont"]/span/text()')[0])
                    single["wfjfs"] = int(x.xpath('div[@class="cbp_tmlabel"]/p[@class="cont"]/span/text()')[1])
                    single["wfsj"] = x.xpath('div[@class="cbp_tmlabel"]/p[@class="box"]/time/text()')[0]
                    clbj = x.xpath('div[@class="cbp_tmlabel"]/p[@class="box"]/span/text()')[0]
                    if "未" in clbj:
                        single["clbj"] = 0
                    elif "已" in clbj:
                        single["clbj"] = 1
                    else:
                        single["clbj"] = 9
                    result["result"].append(single)
                print(result)
            return result
        except Exception as e:
            print(e)
            return {"code": 500, "msg": "暂无法查询！"}


if __name__ == '__main__':
    p = SD()
    info = {"hpzl": "02", "hphm": "鲁CQQ358", "cjh": "260058", "fdjh": "453676"}
    p.get_data(info)
