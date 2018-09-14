import requests
from lxml import etree
from fake_useragent import UserAgent
import csv
import random
import time


def get_python_projects(page):
    # 随机生成UserAgent
        ua = UserAgent()
        headers = {
            'user-agent': ua.chrome
        }
        url = "https://www.hellogithub.com/periodical/category/Python%20%E9%A1%B9%E7%9B%AE/?page={page}".format(page=page)
        response = requests.get(url, headers=headers)
        return response.text


# 解析方法
def parse_python_projects(html):
    data = etree.HTML(html)
    main = data.xpath('//*[@id="main"]/div[2]')
    # print(main)
    # 计算每页items数
    items = data.xpath('//*[@id="main"]/div[2]/h2')
    # print(len(items))
    # ------------------
    for i in range(1, len(items)):
        title = main[0].xpath('./h2[{i}]/a[2]/text()'.format(i=i))
        description = ''.join(main[0].xpath('./p[{i}]/text()'.format(i=i)))
        info = {
            'title': title[0],
            'description': description.strip(),
            'programming_language': 'Python'
        }
        print(info)
        save_to_csv(info)


def save_to_csv(info):
    with open('hello-github.csv', 'a', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'description', 'programming_language']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(info)


if __name__ == '__main__':
    for i in range(1, 30):
        print('正在爬取第{page}页'.format(page=i))
        try:
            html = get_python_projects(i)
            parse_python_projects(html)
            random_sec = random.randint(1, 4)
            print("休眠", random_sec, "秒")
            time.sleep(random_sec)
        except Exception:
            pass