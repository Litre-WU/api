from lxml import etree
import requests


class ZJXCD:
	
	async def get_data(self, info):
		headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
		}
		if info["jdsbh"][:4] == "3301":
			data = {
				"noticeno": "000407" + info["jdsbh"],
				"channelNo": "000407",
				"originalNo": info["jdsbh"],
			}
		elif info["jdsbh"][:4] == "3303":
			data = {
				"noticeno": "330300001" + info["jdsbh"],
				"channelNo": "330300001",
				"originalNo": info["jdsbh"],
			}
		elif info["jdsbh"][:4] == "3304":
			data = {
				"noticeno": "904401" + info["jdsbh"],
				"channelNo": "904401",
				"originalNo": info["jdsbh"],
			}
		elif info["jdsbh"][:4] == "3305":
			data = {
				"noticeno": "330500001" + info["jdsbh"],
				"channelNo": "330500001",
				"originalNo": info["jdsbh"],
			}
		elif info["jdsbh"][:4] == "3306":
			data = {
				"noticeno": "330600001" + info["jdsbh"],
				"channelNo": "330600001",
				"originalNo": info["jdsbh"],
			}
		elif info["jdsbh"][:4] == "3307":
			data = {
				"noticeno": "907401" + info["jdsbh"],
				"channelNo": "907401",
				"originalNo": info["jdsbh"],
			}
		else:
			return {"code": 400, "msg": "该城市咱无法查询！"}
		rs = requests.post(url='http://pay.zjzwfw.gov.cn/payinasync/getNoticenoByBusinesscode.htm', headers=headers,
		                   data=data)
		# print(rs.json())
		data = {
			"single_search_noticeno": rs.json().get("data"),
			"isNoUser": "1"
		}
		rs = requests.post(url='http://pay.zjzwfw.gov.cn/payin/dosearchpayment.htm', headers=headers, data=data)
		# print(rs.text)
		html = etree.HTML(rs.text)
		try:
			table = html.xpath('//table//td/text()')
			
			data = {}
			data['wfsj'] = table[11]
			data['jkdh'] = table[1]
			data['xh'] = table[1]
			# data['xzqu'] = table[3]
			# data['zsda'] = table[5]
			# data['zsdamc'] = table[7]
			data['dsr'] = table[9]
			data['fkje'] = int(float(table[-1]))
			
			wfxwzt = html.xpath('//div[@id="fjContent"]/text()')[1].strip("违法内容:").split(',')
			# print(table, wfxwzt)
			if "无" not in wfxwzt[0]:
				data['hphm'] = wfxwzt[0]
				data['wfsj'] = wfxwzt[1].strip('于') + ":00"
				data['wfdz'] = wfxwzt[2].strip('在')
				data['wfxwzt'] = wfxwzt[3].split('.')[0]
			
			self.result = {"code": 200, "msg": "查询成功！"}
			self.result["result"] = []
			self.result["result"].append(data)
		except:
			self.result = {"code": 200, "msg": "您所查询的缴款单已经缴款或无此文书号！"}
		return self.result


if __name__ == '__main__':
	p = ZJXCD()
	# p.info = {""jdsbh": "3301051420155433"}
	# p.info = {"jdsbh": "3304832100010724"}
	# p.info = {"jdsbh": "3305001216403611"}
	# p.info = {"jdsbh": "3306831323004732"}
	# p.info = {""jdsbh": "3307821963291206"}
	info = {"jdsbh": "3301221450368030"}
	rs = p.get_data(info)
	print(rs)
