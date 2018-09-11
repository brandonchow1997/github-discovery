import requests
from lxml import etree
import pymongo
import time


def login(page):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/47.0.2526.108 Safari/537.36 2345Explorer/8.8.0.16453 '
    }
    cookie = {
        # cookie修改自己的GitHubcookie值
        # user_session为记录用户登录状态的cookie
        'user_session': '自己的cookie值',
    }
    url = 'https://github.com/discover?utf8=%E2%9C%93&recommendations_after=' + str(page * 20)
    response = requests.get(url, headers=header, cookies=cookie)
    print(response.status_code)
    print('-' * 20)
    return response.text


def parse_page(html):
    data = etree.HTML(html)
    title = data.xpath('/html/body/div[4]/div[1]/div/h1/text()')
    items = data.xpath('//*[@id="recommended-repositories-container"]/div/div')
    print(title[0])
    print('|'*40)
    for item in items:
        owner = item.xpath('./div[2]/div[2]/div/div[1]/h3/a/span/text()')
        repository = item.xpath('./div[2]/div[2]/div/div[1]/h3/a/text()')
        contents = item.xpath('./div[2]/div[2]/div/p[@itemprop="description"]/text()')
        # topics = item.xpath('./div[2]/div[2]/div/div[2]/a/text()')
        stars = item.xpath('./div[2]/div[2]/div/div[@class="f6 text-gray mt-2"]/a/text()')
        programming_language = item.xpath('./div[2]/div[2]/div/div[@class="f6 text-gray mt-2"]/span[2]/text()')
        updated = item.xpath('./div[2]/div[2]/div/div[@class="f6 text-gray mt-2"]/relative-time/text()')
        # repository 字符串连接
        info = ''.join(owner).join(repository).strip()
        print(info)
        # description 字符串连接
        content = ''.join(contents).strip()
        print('description:', content)
        # stars
        print('stars:', end='')
        print(stars[1].strip())
        #for topic in topics:
            #print(topic, end=',')
        # programming_language
        programming_language = ''.join(programming_language).strip()
        print('programming_language:', programming_language)
        print('Updated:', updated[0])

        result = {
            'repository': info,
            'description': content,
            'stars': stars[1],
            'programming_language': programming_language,
            'updated': updated[0]
        }
        # 如只需要测试，则注释掉存储语句
        save_to_mongo(result)
        print('-'*10)


def save_to_mongo(result):
    # 保存到MongoDB中
    try:
        if db[MONGO_COLLECTION].insert(result):
            print('存储到 MongoDB 成功')
    except Exception:
        print('存储到 MongoDB 失败')


# MongoDB连接配置
MONGO_URL = 'localhost'
MONGO_DB = 'github_spider'
MONGO_COLLECTION = 'Discover_repositories'
client = pymongo.MongoClient(MONGO_URL, port=27017)
db = client[MONGO_DB]

# 仅爬取10页，可修改
MAX_PAGE = 10
if __name__ == '__main__':
    for page in range(0, MAX_PAGE):
        try:
            print('-- 正在爬取第{page}页 --'.format(page=page+1))
            html = login(page)
            parse_page(html)
            time.sleep(2)
        except Exception:
            pass
