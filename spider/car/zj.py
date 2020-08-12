import requests
from random import randint
import re
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
from tools.chaojiying import Chaojiying_Client


class ZJ:

    def verify_code(self):

        index_url = 'http://www.zjsgat.gov.cn:8087/was/phone/carIllegalQuery.jsp'

        with requests.Session() as session:
            session.headers.update({"User-Agent": f"Mozilla/5.0 (Linux; Android {randint(2,10)}.0; LND-AL30 Build/HONORLND-AL30; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/044611 Mobile Safari/537.36 MMWEBID/472 MicroMessenger/7.0.4.1420(0x27000439) Process/tools NetType/WIFI Language/zh_CN", })
            with session.get(index_url) as index:
                # print(index.text)
                pattern = re.compile(r'.*?tblname=(.*?)"')
                tblname = re.findall(pattern, index.text)[0]
                # print(tblname)
            capture_url = 'http://www.zjsgat.gov.cn:8087/was/Kaptcha.jpg?0'

            with session.get(capture_url) as capture:

                # with open('zj.png', "wb+") as img:
                #     img.write(capture.content)

                cjy = Chaojiying_Client()
                result = cjy.PostPic(capture.content, 1902)
                if result.get("err_no") == -1005:
                    print(result.get("err_str"))
                    return result.get("err_str")
                else:
                    yzm = result.get("pic_str")

            # yzm = input("请输入验证码:")

            verify_url = 'http://www.zjsgat.gov.cn:8087/was/portals/checkManyYzm.jsp'
            with session.post(url=verify_url, data={"randValue": yzm}) as rs:
                # print(rs.text)
                if rs.json()["result"] == "Y":
                    # rs = {"session": session, "tblname": tblname, "yzm": yzm}
                    return session, tblname, yzm
                else:
                    return self.verify_code()

    async def get_data(self, info):
        session, tblname, yzm = self.verify_code()

        url = f'http://www.zjsgat.gov.cn:8087/was/common.do?tblname={tblname}%25E6%25B5%2599{info["hphm"][1:]}&carno={info["cjh"]}&cartype={info["hpzl"]}&carTypeValue=%D0%A1%D0%CD%C6%FB%B3%B5&yzm={yzm}'
        try:
            with session.post(url) as rs:
                # print(rs.text)
                html = etree.HTML(rs.text)
                spans = html.xpath('//table[@align="center"]/tr/td/span/text()')
                # print(spans)
                results = {"code": 200, "msg": "成功！", "result": []}
                if "无非现场违法记录" in spans[0]:
                    return results
                single = {}
                single["wfdz"] = spans[5]
                single["wfxwzt"] = spans[7].strip()
                single["wfsj"] = spans[9].strip()
                clbj = spans[11]
                if "未" in clbj:
                    single["clbj"] = 0
                elif "已" in clbj:
                    single["clbj"] = 1
                else:
                    single["clbj"] = 9
                jkbj = spans[13]
                if "未" in jkbj:
                    single["jkbj"] = 0
                elif "已" in jkbj:
                    single["jkbj"] = 1
                else:
                    single["jkbj"] = 9
                single["cjjg"] = spans[15]
                results["result"].append(single)

                total = int(html.xpath('//table/tr/td/span/span/text()')[0])
                # print(total)
                if total > 1:
                    meta = {"session": session, "result": results}
                    with ThreadPoolExecutor(total) as exector:
                        for p in range(1, total):
                            meta["p"] = str(p)
                            exector.submit(self.get_next, meta)
                # print(meta["result"])
                return meta["result"]
        except Exception as e:
            print(e)
            return {"code": 500, "msg": "暂无法查询！"}

    def get_next(self, meta):

        next_url = 'http://www.zjsgat.gov.cn:8087/was/phone/carIllegalQueryResult.jsp?currentpage=' + meta["p"]
        # print(next_url)
        with meta["session"].post(next_url) as rs:
            # print(rs.text)
            html = etree.HTML(rs.text)
            spans = html.xpath('//table[@align="center"]/tr/td/span/text()')
            # print(spans)
            if spans:
                single = {}
                single["wfdz"] = spans[5]
                wfxwzt = spans[7].strip()
                if "违" in wfxwzt:
                    single["wfxwzt"] = None
                    single["wfsj"] = spans[8].strip()
                    clbj = spans[10]
                    if "未" in clbj:
                        single["clbj"] = 0
                    elif "已" in clbj:
                        single["clbj"] = 1
                    else:
                        single["clbj"] = 9
                    jkbj = spans[12]
                    if "未" in jkbj:
                        single["jkbj"] = 0
                    elif "已" in jkbj:
                        single["jkbj"] = 1
                    else:
                        single["jkbj"] = 9
                    single["cjjg"] = spans[14].strip()
                    # print(single)
                    meta["result"]["result"].append(single)
                else:
                    single["wfsj"] = spans[9].strip()
                    clbj = spans[11]
                    if "未" in clbj:
                        single["clbj"] = 0
                    elif "已" in clbj:
                        single["clbj"] = 1
                    else:
                        single["clbj"] = 9
                    jkbj = spans[13]
                    if "未" in jkbj:
                        single["jkbj"] = 0
                    elif "已" in jkbj:
                        single["jkbj"] = 1
                    else:
                        single["jkbj"] = 9
                    single["cjjg"] = spans[15].strip()
                    # print(single)
                    meta["result"]["result"].append(single)


if __name__ == '__main__':
    p = ZJ()
    info = {'hphm': '浙EYW231', "hpzl": "02", 'cjh': '272938', 'fdjh': 'U67447'}
    rs = p.get_data(info)
    print(rs)
