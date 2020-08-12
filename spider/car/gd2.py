from random import randint
import requests


class GD2:
	
	async def get_data(self, info):
		url = 'https://yjmtpt.xx-motor.com/gateway/jmt-api/getCarViolation'
		headers = {
			"xmd-gateway-authorization": "yjmtwechat-xx-motor",
			"User-Agent": "Mozilla/5.0 (Linux; Android 8.0.0; LND-AL30 Build/HONORLND-AL30; wv) AppleWebKit/537.36 (KHTML, "
			              "like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/044611 Mobile Safari/537.36 MMWEBID/472 MicroMessenger/7.0.4.1420(0x2700043A) Process/tools NetType/WIFI Language/zh_CN",
			"Content-Type": "application/x-www-form-urlencoded",
			"Referer": "https://yjmtpt.xx-motor.com/wechat/index.html",
			"X-Forwarded-For": str(randint(1, 255)) + '.' + str(randint(1, 255)) + '.' + str(
				randint(1, 255)) + '.' + str(randint(1, 255))
		}
		data = {
			"plate_no": info["hphm"][1:],
			"car_type": info["hpzl"],
			"eng_no": info["fdjh"][-6:],
		}
		with requests.get(url='http://124.172.189.180:5010/get/') as ip:
			proxies = {"http": ip.text}
		with requests.post(url=url, headers=headers, data=data, proxies=proxies)as rs:
			# print(rs.text)
			try:
				rd = rs.json()
				if not rd["err_code"]:
					result = {"code": 200, "msg": "成功！", "result": []}
					for x in rd["result_set"]:
						single = {}
						single["wfsj"] = x["wfsj"]
						single["wfdz"] = x["wfdz"]
						single["wfxwzt"] = x["wfxw"]
						single["cjjgmc"] = x["cjjgmc"]
						single["wfjfs"] = x["wfjfs"]
						single["znj"] = x["znj"]
						single["clbj"] = int(x["clbj"])
						single["jkbj"] = int(x["jkbj"])
						single["fkje"] = int(x["fkje"])
						single["jdsbh"] = x["jdsbh"]
						
						result["result"].append(single)
					return result
				else:
					return {"code": 400, "msg": "车辆信息错误！"}
			except Exception as e:
				print(e)
				return {"code": 500, "msg": "暂无法查询！"}


if __name__ == '__main__':
	p = GD2()
	info = {"hpzl": "02", "hphm": "粤A1QH04", "fdjh": "444639"}
	rs = p.get_data(info)
	print(rs)
