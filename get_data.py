import json
import time
import requests
from collections import defaultdict

from lxml import etree


data = defaultdict(dict)


def _crawl(url):

    headers = {
        "Accept": "*/*",
        "Referer": "https://www.xzw.com/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    }

    res = requests.get(url, headers=headers)
    dom = etree.HTML(res.content)

    title = dom.xpath('//div[@class="top"]/a[@class="on"]/text()')
    nodes = dom.xpath('//div[@class="c_cont"]/p/span/text()')
    return f"{title[0]}：{nodes[0]}"


def crawl(code):
    urls = {
        "今": f"https://www.xzw.com/fortune/{code}/",
        "明": f"https://www.xzw.com/fortune/{code}/1.html",
        "周": f"https://www.xzw.com/fortune/{code}/2.html",
        "月": f"https://www.xzw.com/fortune/{code}/3.html",
        "年": f"https://www.xzw.com/fortune/{code}/4.html",
    }
    for t, url in urls.items():
        data[code][t] = _crawl(url)


if __name__ == "__main__":

    # _crawl("https://www.xzw.com/fortune/gemini/")

    for code in ["aries", "taurus", "gemini", "cancer", "leo", "virgo",
                 "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"]:
        crawl(code)

    with open("horoscope_data.json", "w") as outfile:
        json.dump(data, outfile, ensure_ascii=False)

