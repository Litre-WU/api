from concurrent.futures import ThreadPoolExecutor
from lxml import etree
from urllib.parse import quote
import requests
import time
import asyncio


class BJ:

    def get_cookie(self, headers):
        url = 'https://fee.icbc.com.cn/servlet/AsynGetDataServlet'
        data = "tranFlag=0&totalInPage=3&currentPage=1&QueryType_in=&QueryChannel_in=openEbankFlag&QueryArea_in=0200&QueryKeyWord_in=&tranCode=p00021"
        headers["Cookie"] = \
            requests.post(url=url, headers=headers, data=data).headers.get("Set-Cookie").split(";")[0]

        data = "pageMark=1&paymentContent=&queryPageinfo=1&netType=181&IEVersionFlag=0&ComputID=10&PlatFlag=0&areaCodeTmp=0200&areaNameTmp=%B1%B1%BE%A9&dse_menuid=PM002&IN_PAYITEMCODE=PJ160016011000008607&isShortpay=&maskFlag=0&isP3bank=0"
        rs = requests.post(url='https://fee.icbc.com.cn/servlet/ICBCINBSEstablishSessionServlet', headers=headers,
                           data=data)
        # print(rs.text)
        html = etree.HTML(rs.text)
        dse_sessionId = html.xpath('//form/input[@name="dse_sessionId"]/@value')[0]
        # print(dse_sessionId)
        return headers, dse_sessionId

    async def get_data(self, info):
        url = 'https://fee.icbc.com.cn/icbc/conformity/forward.jsp'
        headers = {
            "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E)",
            "Content-Type": "application/x-www-form-urlencoded",
            # "Cookie": "SRV_EBANKP_EPAY_APP=ebankpapp-node3-wgq-3038127248-chskc-84.105.110.185-35041|XL5nc|XL5mn"
        }
        headers, dse_sessionId = self.get_cookie(headers)

        data = {
            "dse_sessionId": dse_sessionId,
            "sCardNo": "6222370074801149",
            "sCarCode": info["hphm"][1:],
            "sEngineNo": info["fdjh"],
            "url": "/TransferApp/forward.jsp?id=/traffic/TrafficFinesNolive.do&sAppZone=00200",
        }
        
        rs = requests.post(url=url, headers=headers, data=data)
        # print(rs.text)
        result = {"code": 200, "msg": "查询成功！", "result": []}

        try:

            html = etree.HTML(rs.text)
            detail_url_list = html.xpath('//table/tr/td/a/@href')
            # print(detail_url_list)
            with ThreadPoolExecutor(5) as exector:
                [exector.submit(self.get_detail, url[x], headers, result) for x in range(len(detail_url_list))]
                # for x in range(len(detail_url_list)):
                #     exector.submit(self.get_detail, detail_url_list[x], headers, result)
            # print(len(detail_url))
    
            inputs = html.xpath('//form/input')

            html.xpath('//form/input[@name="sCustName"]/@value')[0]

            data = {}
            for x in inputs:
                # print(x.xpath('@name'),x.xpath('@value'))
                data[x.xpath('@name')[0]] = x.xpath('@value')[0]
            # print(data)
            meta = {
                "data": data,
                "headers": headers,
                "result": result
            }
            # total = int(html.xpath('//font/text()')[0].split("，")[-1].replace("共", "").replace("条", ""))
            # print(total)
            # get_next(meta)

            coroutine = self.get_next(meta)
            task = asyncio.ensure_future(coroutine)
            loop = asyncio.get_event_loop()
            loop.run_until_complete(task)
        except Exception as e:
            return result

        return result

    def get_detail(self, url, headers, result):
        url = 'https://fee.icbc.com.cn' + url
        # print(url)
        headers = headers
        # print(headers)
        rs = requests.get(url=url, headers=headers)
        # print(rs.text)
        single = {}
        html = etree.HTML(rs.text)
        inputs = html.xpath('//form/input/@value')
        # print(inputs)
        single["hphm"] = info["hphm"]
        single["hpzl"] = inputs[3]
        single["fdjh"] = info["fdjh"]
        single["jszdabh"] = inputs[5]
        single["jszsjh"] = inputs[9]
        single["jszh"] = inputs[10]
        single["xszczxm"] = inputs[12]
        single["xh"] = inputs[15]
        single["wfsj"] = inputs[16][:10] + " " + inputs[16][11:]
        single["wfxw"] = inputs[17]
        single["wfxwzt"] = inputs[18]
        single["fkje"] = int(inputs[19][:-2])
        # single["znj"] = inputs[20][:-2]
        single["wfcs"] = inputs[22]
        single["wfdz"] = inputs[23]
        single["wfjfs"] = int(inputs[24])

        result["result"].append(single)
        # print(result)

    async def get_next(self, meta):
        # print(meta)
        data = meta["data"]
        data["flag"] = "next"
        data["sCustName"] = quote(data["sCustName"])
        data["url"] = "/TransferApp/forward.jsp?id=/traffic/TrafficFinesNolive.do&sAppZone=00200"
        # data = f'flag=next&sNo={meta["data"]["sNo"]}&sSerial_No={meta["data"]["sSerial_No"]}&sSTARTTIME={meta["data"][
        #     "sSTARTTIME"]}&sCardNo={meta["data"]["sCardNo"]}&sCARCODE={meta["data"]["sCARCODE"]}&sENGINENO={meta["data"][
        #     "sENGINENO"]}&sSumItem={meta["data"]["sSumItem"]}&sCustName={quote(meta["data"]["sCustName"])}&sDriver_No={
        # meta["data"]["sDriver_No"]}&dse_sessionId={meta["data"][
        #     "dse_sessionId"]}&url=/TransferApp/forward.jsp?id=/traffic/TrafficFinesNolive.do&sAppZone=00200'
        rs = requests.post(url='https://fee.icbc.com.cn/icbc/conformity/forward.jsp', headers=meta["headers"],
                           data=data)

        # print(rs.text)
        html = etree.HTML(rs.text)
        detail_url_list = html.xpath('//table/tr/td/a/@href')
        # print(detail_url_list)
        with ThreadPoolExecutor(5) as exector:
            for url in detail_url_list:
                exector.submit(self.get_detail, url, meta["headers"], meta["result"])

        try:
            html.xpath('//form/input[@name="sCustName"]/@value')[0]
            inputs = html.xpath('//form[@name="nextPageForm"]/input')

            data = {}
            for x in inputs:
                # print(x.xpath('@name'),x.xpath('@value'))
                data[x.xpath('@name')[0]] = x.xpath('@value')[0]
            # print(data)
            meta["data"] = data
            # get_next(meta)
            await self.get_next(meta)
        except Exception as e:
            return meta


if __name__ == '__main__':
    # info = {"kh": "6222370074801149", "hphm": "京FR3568", "fdjh": "749475AVQ25"}
    info = {"hphm": "京Q32EB1", "fdjh": "A3030243"}

    s = time.clock()
    p = BJ()
    rs = p.get_data(info)
    print(rs)
    print(time.clock() - s)

    # get_cookie()
