import requests
from spider.tools.headers import ua
from lxml import etree
from concurrent.futures.thread import ThreadPoolExecutor

url_list = ['http://265zy.cc', 'http://123ku.com', 'http://okzyw.com', 'http://www.zuidazy1.net', 'http://chaojizy.com',
            'http://kankanzy.com', 'http://666zy.com']


class Movie:
    def __init__(self):
        self.data = []
        self.info = {}

    def mul_col(self, url):
        params = {"m": "vod-search"}
        data = {
            "wd": self.info.get("keyword", ""),
            "submit": "search"
        }
        headers = ua()
        try:
            with requests.post(url=url, params=params, data=data, headers=headers, timeout=2) as rs:
                # print(rs.text)
                html = etree.HTML(rs.text)
                hrefs = html.xpath('//span[@class="xing_vb4"]/a/@href')
                # print(hrefs)
            if hrefs:
                with ThreadPoolExecutor(len(hrefs)) as exector:
                    exector.map(self.parse_data,
                                [{"headers": headers, "url": url, "href": hrefs[x]} for x in range(len(hrefs))])
                    # for x in range(len(hrefs)):
                    #     exector.submit(self.parse_data({"headers": headers, "url": url, "href": href[x]}))
            return self.data
        except:
            pass

    def parse_data(self, meta):
        if meta["href"]:
            url = meta["url"] + meta["href"]
            try:
                with requests.get(url, headers=meta["headers"], timeout=2) as rs:
                    html = etree.HTML(rs.text)
                    play = html.xpath('//div[@class="vodplayinfo"]/div/ul/li/text()')
                    if not play:
                        play = html.xpath('//div[@class="vodplayinfo"]/div/div/ul/li/text()')
                        if not play:
                            play = html.xpath('//div/div/ul/li/a/text()')
            except:
                return 0
            play_list = []
            if len(play) == 1:
                if "m3u8" in play[0][-4:]:
                    play_list.append({
                        "m3u8": {play[0].split("$")[0]: play[0].split("$")[1]}
                    })
            elif "mp4" in play[int(len(play) / 3) + 1][-3:]:
                if "m3u8" in play[0][-4:]:
                    play_list.append({
                        "m3u8": {p.split("$")[0]: p.split("$")[1] for p in play[0:int(len(play) / 3)]},
                        "src": {p.split("$")[0]: p.split("$")[1] for p in
                                play[int(len(play) / 3):int(len(play) * 2 / 3)]},
                        "download": {p.split("$")[0]: p.split("$")[1] for p in play[int(len(play) * 2 / 3):]}
                    })
                else:
                    play_list.append({
                        "src": {p.split("$")[0]: p.split("$")[1] for p in play[0:int(len(play) / 3)]},
                        "m3u8": {p.split("$")[0]: p.split("$")[1] for p in
                                 play[int(len(play) / 3):int(len(play) * 2 / 3)]},
                        "download": {p.split("$")[0]: p.split("$")[1] for p in play[int(len(play) * 2 / 3):]}
                    })
            elif "m3u8" in play[0][-4:]:
                play_list.append({
                    "m3u8": {p.split("$")[0]: p.split("$")[1] for p in play[0:int(len(play) / 2)]},
                    "src": {p.split("$")[0]: p.split("$")[1] for p in play[int(len(play) / 2):]}
                })
            else:
                play_list.append({
                    "src": {p.split("$")[0]: p.split("$")[1] for p in play[0:int(len(play) / 2)]},
                    "m3u8": {p.split("$")[0]: p.split("$")[1] for p in play[int(len(play) / 2):]}
                })
            # print(play_list)
            self.data.append({"name": self.info["keyword"], meta["url"]: play_list})
            return self.data

    async def run(self, info):
        self.info = info
        with ThreadPoolExecutor(len(url_list)) as exector:
            exector.map(self.mul_col, url_list)
            # for x in range(len(url_list)):
            #     exector.submit(self.mul_col(url_list[x]))
        # print(self.data)
        return self.data


source_list = ['http://265zy.cc', 'http://123ku.com']
source_url = source_list[0]


async def search_movie(info):
    if info["keyword"]:
        keyword = info.get("keyword", "")
        url = f'{source_url}/index.php'
        params = {
            "m": "vod-search",
        }
        data = {
            "wd": keyword,
            "submit": "search"
        }
        headers = ua()
        try:
            with requests.post(url=url, params=params, data=data, headers=ua()) as rs:
                html = etree.HTML(rs.text)
                names = html.xpath('//span[@class="xing_vb4"]/a/text()')
                links = html.xpath('//span[@class="xing_vb4"]/a/@href')

                context = {
                    'title': "搜索",
                    'url': '/movie/search/',
                    "result": []
                }
                for index, l in enumerate(links):
                    url = source_url + l
                    with requests.get(url=url, headers=headers) as rs:
                        # print(rs.text)
                        html = etree.HTML(rs.text)
                        pnames = html.xpath('//div/div/ul/li/a/text()')
                        pnames = [n.split("$")[0] for n in pnames]
                        plinks = html.xpath('//div/div/ul/li/a/@href')
                        n = int(len(plinks) / 2)
                        if "m3u8" in plinks[0]:
                            info_1 = dict(zip(pnames[:n], plinks[:n]))
                            info_2 = dict(zip(pnames[n:], plinks[n:]))
                        else:
                            info_2 = dict(zip(pnames[:n], plinks[:n]))
                            info_1 = dict(zip(pnames[n:], plinks[n:]))
                        data = {
                            "name": names[index],
                            "play": info_1,
                            "play_url": info_2
                        }
                        context["result"].append(data)
            result = context
        except Exception as e:
            result = {
                "msg": "抱歉！暂时无法搜索",
                "result": []
            }
    else:
        result = {
            "msg": "请输入关键字",
            "result": []
        }

    return result


if __name__ == '__main__':
    p = Movie()
    rs = p.run()
    print(rs)

    # p.mul_col(url='http://kankanzy.com')
