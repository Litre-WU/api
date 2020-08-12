import requests
from tools.chaojiying import Chaojiying_Client
import time


class SC:
	
	def verify(self):
		headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"}
		with requests.get(url='http://124.172.189.180:5010/get/') as ip:
			proxies = {"http": ip.text}
		with requests.session()as session:
			session.headers = headers
			session.proxies = proxies
			with session.get(url=f'http://gat.sc.gov.cn/wsga/query/car/captcha?d={str(int(time.time() * 1000))}')as img:
				# with open('sc.png', "wb+")as f:
				# 	f.write(img.content)
				cjy = Chaojiying_Client()
				result = cjy.PostPic(img.content, 1902)
				if result.get("err_no") == -1005:
					print(result.get("err_str"))
					return result.get("err_str")
				else:
					yzm = result.get("pic_str")
				# print(yzm)
				return session, yzm
	
	async def get_data(self, info):
		
		session, yzm = self.verify()
		url = 'http://gat.sc.gov.cn/wsga/query/car/doquery'
		
		data = {
			"cartype": info["hpzl"],
			"cararea": "川",
			"carnum": info["hphm"][1:],
			"carenginenum": info["fdjh"][-6:],
			"checkcode": yzm,
			"type": "1",
		}
		with session.post(url=url, data=data) as rs:
			# print(rs.text)
			res = {"code": 200, "msg": "成功！", "result": []}
			if rs.json()["state"] == "400":
				return await self.get_data(info)
			elif rs.json()["state"] == "0":
				data = rs.json()["data"]
				if data:
					for x in data:
						single = {}
						single["hphm"] = info["hphm"]
						single["hpzl"] = info["hpzl"]
						single["cjh"] = info.get("cjh", "")
						single["fdjh"] = info["fdjh"]
						single["xh"] = x["xh"]
						single["wfsj"] = x["wfsj"]
						single["wfdz"] = x["wfdz"]
						single["wfxwzt"] = x["wfxw"]
						single["wfxw"] = x["wfdh"]
						single["wfjfs"] = x["jf"]
						single["fkje"] = int(x["fkje"])
						single["clbj"] = int(x["clbj"])
						single["jkbj"] = int(x["jkbj"])
						res["result"].append(single)
					return res
				else:
					return res
			else:
				res["code"] = 400
				res["msg"] = rs.json()["msg"]
				return res


if __name__ == '__main__':
	p = SC()
	info = {"hpzl": "02", "hphm": "川A3L70V", "cjh": "102968", "fdjh": "116297"}
	rs = p.get_data(info)
	print(rs)
