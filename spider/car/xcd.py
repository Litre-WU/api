from spider.car.xcd_zj import ZJXCD
from concurrent.futures import ThreadPoolExecutor
import requests
import redis


class XCD:
	# redis_db = redis.Redis(host="localhost", port=6379, password='wl98pyth04', db=0, decode_responses=True)
	pool = redis.ConnectionPool(host='124.172.189.180', port=6379, db=1, password='wl98pyth04', decode_responses=True)
	conn = redis.StrictRedis(connection_pool=pool)
	
	async def action(self, info):
		
		jdsbh2city = {
			'bj': 11,
			'tj': 12,
			'he': 13,
			'sx': 14,
			'nm': 15,
			'ln': 21,
			'jl': 22,
			'hl': 23,
			'sh': 31,
			'nkg': 3201,
			'wux': 3202,
			'xuz': 3203,
			'czx': 3204,
			'szv': 3205,
			'ntg': 3206,
			'lyg': 3207,
			'has': 3208,
			'ynz': 3209,
			'yzo': 3210,
			'zhe': 3211,
			'tzs': 3212,
			'suq': 3213,
			'hgh': 3301,
			'ngb': 3302,
			'wnz': 3303,
			'jix': 3304,
			'hzh': 3305,
			'sxg': 3306,
			'jha': 3307,
			'quz': 3308,
			'zos': 3309,
			'tzz': 3310,
			'lss': 3311,
			'zjgs': 33,
			'ah': 34,
			'fj': 35,
			'jx': 36,
			'sd': 37,
			'ha': 41,
			'hb': 42,
			'hn': 43,
			'gd': 44,
			'gx': 45,
			'hi': 46,
			'cq': 50,
			'sc': 51,
			'gz': 52,
			'yn': 53,
			'xz': 54,
			'sn': 61,
			'gs': 62,
			'qh': 63,
			'nx': 64,
			'xj': 65,
		}
		
		if info["jdsbh"][:2] == "33":
			try:
				p = ZJXCD()
				result = await p.get_data(info=info)
				info["result"] = result
				return info
			except Exception as e:
				info["result"] = {"code": 400, "msg": "获取数据失败！请稍后查询。。。"}
				return info
		
		try:
			info["city"] = list(jdsbh2city.keys())[list(jdsbh2city.values()).index(int(info["jdsbh"][:2]))]
			return self.parse_data(info)
		except Exception as e:
			info["city"] = list(jdsbh2city.keys())[list(jdsbh2city.values()).index(int(info["jdsbh"][:4]))]
			return self.parse_data(info)
	
	def parse_data(self, info):
		
		try:
			if len(info["jdsbh"]) == 15:
				# {'message': '决定书格式不正确', 'code': 500}
				last_num = [x for x in range(10)]
				last_num.append('X')
				with ThreadPoolExecutor(11) as executor:
					for x in last_num:
						info["last"] = x
						executor.submit(self.get_data, info)
			else:
				info["last"] = ''
				self.get_data(info)
		
		except Exception as e:
			# print(e)
			return {"code": 400, "msg": "获取数据失败！请稍后查询。。。"}
	
	def get_data(self, info):
		
		url = f'https://{info["city"]}.122.gov.cn/vio/violation/list.do'
		data = {
			"jdsbh": info["jdsbh"] + str(info["last"]),
			"page": "1",
			"size": "10"
		}
		sessionid = self.conn.hmget("data1", info["city"])
		sessionid = sessionid[0] if sessionid else ''
		headers = {
			"Accept": "application/json, text/javascript, */*; q=0.01",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
			# "Cookie": f'JSESSIONID-L={self.redis_db.get(info["city"])}'
			"Cookie": f'JSESSIONID-L={sessionid}'
		}
		# print(data)
		rs = requests.post(url=url, headers=headers, data=data, timeout=5)
		# print(rs.text)
		try:
			if rs.json().get("code") == 200:
				info["result"] = {"code": 200, "msg": "查询成功！", "result": []}
				if rs.json()["data"]["content"]:
					for x in rs.json()["data"]["content"]:
						single = {}
						single["wfsj"] = x.get("wfsj", "") + ":00"
						single["wfdz"] = x.get("wfdz", "")
						single["wfjfs"] = int(x.get("zffs", ""))
						single["wfxw"] = x.get("wfxw", "")
						single["hpzl"] = x.get("hpzl", "")
						single["hphm"] = x.get("hphm", "")
						single["fkje"] = int(x.get("fkje", ""))
						single["xh"] = x.get("jdsbh", "")
						single["jdsbh"] = x.get("jdsbh", "")
						single["clsj"] = x.get("clsj", "") + ":00"
						single["violationLatefine"] = int(x.get("znj", ""))
						single["xxly"] = 2
						single["dsr"] = x.get("dsr", "")
						
						info["result"]["result"].append(single)
				else:
					return info
			elif rs.json().get("code") == 500:
				pass
			else:
				info["result"] = {"code": 401, "msg": "未查到相关数据"}
			return info
		except Exception as e:
			info["result"] = {"code": 402, "msg": "未查到相关数据"}
			return info


if __name__ == '__main__':
	p = XCD()
	info = {"city": "he", "jdsbh": "1305811500250741"}
	# info = {"city": "xuz", "jdsbh": "3203051907262486"}
	# info = {"city":"he","jdsbh":"1307211605639134"}
	# info = {"city":"he","jdsbh":"1307971600135384"}
	# info = {"city":"yn","jdsbh":"5301901506887294"}
	# info = {"city": "yn", "jdsbh": "5301971913971477"}
	# info = {"city": "gd", "jdsbh": "4401101606121282"}
	# info = {"city": "yn", "jdsbh": "530197191401786"}
	# info = {"jdsbh": "321323199496721"}
	# info = {"jdsbh": "3301051420155433"}
	# info = {"jdsbh": "3304832100010724"}
	# info = {"jdsbh": "3101171011008327"}
	# info = {"jdsbh": "6321221000780244"}
	p.action(info)
	print(info["result"])
