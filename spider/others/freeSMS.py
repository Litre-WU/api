import requests
import json
from spider.tools.headers import async_ua


async def sms(info):
    result = {
        "result": []
    }
    url = 'http://www.xnsms.com/test/getPhones'

    with requests.post(url=url, headers=await async_ua()) as rs:
        result["result"] = rs.json()
    return result


async def msg(info):
    result = {
        "result": []
    }
    if info["phone"]:
        phone = info.get("phone", "")

        url = 'http://www.xnsms.com/test/getPhoneData'
        data = {
            "phone": phone,
        }
        headers = ua()
        headers.update({
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip, deflate",
        })
        with requests.post(url=url, data=json.dumps(data), headers=headers) as rs:
            result["result"] = rs.json()

    return result
