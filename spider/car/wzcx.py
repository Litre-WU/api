# coding=utf-8
# 作者      : WU
# 创建时间   : 2019/6/28
# 文件名    : wzcx
# IDE      : PyCharm
import requests
from random import randint
from lxml import etree


class Q:
	def __init__(self):
		pass
	
	async def run(self, info):
		url = 'http://www.cheshenyou.com/portal/vehicleViolationQuery/queryViolation.do'
		headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 " \
			              "Safari/537.36",
			"X-Forwarded-For": str(randint(0, 255)) + "." + str(randint(0, 255)) + "." + str(
				randint(0, 255)) + "." + str(
				randint(0, 255))
		}
		data = {
			"carNum": info.get("hphm", ""),
			"carType": info.get("hpzl", ""),
			"carFrameNum": info.get("cjh", ""),
			"vengineNum": info.get("fdjh", ""),
			"type": "member",
		}
		try:
			with requests.post(url=url, headers=headers, data=data) as rs:
				html = etree.HTML(rs.text)
				trs = html.xpath('//table/tr')[1::]
				total = len(trs)
				# print(len(trs))
				data = []
				detail_name = ['wzsj', 'wzcs', 'wzdd', 'wzxw']
				for x in trs:
					detail = x.xpath('td/dl/dd/text()')
					# print(detail)
					wz = dict(zip(detail_name, detail))
					
					kf = x.xpath('td[@class="subtotal"]/following-sibling::td[1]/text()')[0]
					fj = x.xpath('td[@class="forfeit"]/text()')[0]
					znj = x.xpath('td[@class="latefine"]/text()')[0]
					# print(kf, fj, znj)
					wz['kf'] = kf
					wz['fj'] = fj
					wz['znj'] = znj
					data.append(wz)
				result = {
					"code": 200,
					"msg": "查询成功",
					"total": total,
					"data": data
				}
				return result
		except Exception as e:
			print(e)
			result = {
					"code": 500,
					"msg": "查询失败",
					"total": 0,
					"data": []
				}
			return result


if __name__ == '__main__':
	p = Q()
	info = {"hphm": "川BZR500", "hpzl": "02", "cjh": "015098", "fdjh": "442038"}
	# info = {"hphm": "川ARE123", "hpzl": "02", "cjh": "021638", "fdjh": "406203"}
	# info = {"hphm": "湘D8RR28", "hpzl": "02", "cjh": "595249", "fdjh": "F360007"}
	# info = {"hphm": "沪AUY279", "hpzl": "02", "cjh": "L02572", "fdjh": "14M1700"}
	rs = p.run(info)
	print(rs)
