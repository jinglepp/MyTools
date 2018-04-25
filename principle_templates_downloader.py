# coding:utf-8
import requests
import time
import os
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/65.0.3325.181 Safari/537.36"}
pages = 1  # 总页数
delay = 1  # 延时防被ban


def get_card_url(url):
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, "lxml")
    return filter(lambda i: not i.a["href"].startswith("https://designmodo.com/shop/"),
                  soup.find_all("div", class_=["col-xs-12 col-sm-6 col-md-4 col-lg-3"]))


def get_prd_file_url(url):
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, "lxml")
    return soup.find("select", id="downloadUrl").option["value"]


# 下载prd文件
def download_prd_file(prd_url):
    file_name = os.path.basename(prd_url)
    with open(file_name, "wb") as prd:
        prd.write(requests.get(prd_url, headers=headers).content)


for url in map(lambda page: f"http://principletemplates.com/page/{page}/", range(1, pages + 1)):
    print("开始解析：" + url)
    cards = [card.a["href"] for card in get_card_url(url)]
    print("在当前页面取得链接：\n" + "\n".join(cards))
    for card in cards:
        tmp_url = card
        print("\t开始处理：" + tmp_url)
        prd_url = get_prd_file_url(tmp_url)
        print("\t\t开始下载：" + prd_url)
        try:
            download_prd_file(prd_url)
            print("\t\t下载" + prd_url + "完成！")
        except Exception as e:
            print("\n下载" + prd_url + "失败！" + e)
        time.sleep(delay)  # 延时防止被ban
    print("下载完成！")
