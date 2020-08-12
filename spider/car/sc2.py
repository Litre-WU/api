import requests
from lxml import etree


class SCN:
	
	async def get_data(self, info):
		url = 'http://www.jdcnj.com/wzselect.aspx'
		headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
		}
		# with requests.get(url='http://124.172.189.180:5010/get/') as ip:
		# 	proxies = {"http": ip.text}
		with requests.get(url=url, headers=headers)as index:
			# print(index.text)
			html = etree.HTML(index.text)
			__VIEWSTATE = html.xpath('//input[@id="__VIEWSTATE"]/@value')[0]
			__EVENTVALIDATION = html.xpath('//input[@id="__EVENTVALIDATION"]/@value')[0]
		# print(__VIEWSTATE, __EVENTVALIDATION)
		data = {
			"__VIEWSTATE": __VIEWSTATE,
			"__EVENTVALIDATION": __EVENTVALIDATION,
			"drpCarNumber": info["hphm"][:2],
			"txtCarNumber": info["hphm"][2:],
			"txtCarcode": info["cjh"][-6:],
			"btnSearch": ""
		}
		with requests.post(url=url, headers=headers, data=data)as rs:
			# print(rs.text)
			html = etree.HTML(rs.text)
			result = {"code": 200, "msg": "成功！", "result": []}
			try:
				divs = html.xpath('//div[contains(@style,"font-size: 13px; min-height: 80px;")]')
				for x in divs:
					single = {}
					single["wfsj"] = \
					x.xpath('div/div/div[contains(@style,"font-size: 13px; letter-spacing: 1px; ")]/text()')[0].split("：")[
						-1].strip()
					single["wfdz"] = x.xpath('div/div/div[contains(@style,"font-size: 12px;")]/text()')[0].split("：")[
						-1].strip()
					single["fkje"] = int(x.xpath('div/div/div[contains(@style,"color: #FF9900;")]/text()')[0].split(
						"：")[
						-1].strip())
					single["wfjfs"] = int(x.xpath('div/div/text()')[-1].split("：")[
						-1].strip())
					single["wfxwzt"] = x.xpath('div[contains(@style,"margin-top: 10px; color: Gray")]/text()')[0].strip()
					result["result"].append(single)
				# print(result)
				return result
			except Exception as e:
				print(e)
				return {"code": 400, "msg": "车辆信息错误！"}


if __name__ == '__main__':
	p = SCN()
	info = {"hpzl": "02", "hphm": "川A0784Y", "cjh": "057625"}
	# info = {"hpzl": "02", "hphm": "川A6W17H", "cjh": "038044"}
	rs = p.get_data(info)
	print(rs)
