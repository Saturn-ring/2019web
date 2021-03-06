import requests
import pymongo
import time


# 第一页种子
def get_first_page():
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/69.0.3497.12 Safari/537.36'
    }
    url = 'https://www.zhihu.com/api/v4/members/zhouyuan/followees?include=data%5B*%5D.answer_count' \
          '%2Carticles_count%2Cgender%2C2Cfollowing_count%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(' \
          'type%3Dbest_answerer)%5D.topics&offset=0&limit=20'
    response = requests.get(url, headers=header)
    print(response.status_code)
    return response.json()


def get_page(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/69.0.3497.12 Safari/537.36 '
    }
    response = requests.get(url, headers=header)
    return response.json()


# 解析函数
def parse(html):
    print(html)
    if('data' not in html):
        return 
    items = html['data']
    i=0
    for item in items:
        i=i+1
        name = item['name']
        url_token = item['url_token']
        headline = item['headline']
        badge = item['badge']
        if(len(badge)>0):
            sideItem = badge[0]['description']
        else:
            sideItem = 0
        follower_count = item['follower_count']
        answer_count = item['answer_count']
        gender = item['gender']
        url = 'https://www.zhihu.com/api/v4/members/' + str(url_token) + '/followees?include=data%5B*%5D.answer_count' \
                                                                         '%2Carticles_count%2Cgender%2C2Cfollowing_count%2Cfollower_count' \
                                                                         '%2Cis_followed%2Cis_following%2Cbadge%5B%3F(' \
                                                                         'type%3Dbest_answerer)%5D.topics&offset=0' \
                                                                         '&limit=20 '
        info = {
            'name': name,
            'url_token':url_token,
            'headline':headline,
            'sideItem':sideItem,
            'follower_count': follower_count,
            'gender': gender,
            'answer_count': answer_count   
        }
        print(i)
        print('name', name)
        print('url_token',url_token)
        print('headline', headline)
        print('sideItem',sideItem)
        print('follower_count:', follower_count)
        print('gender', gender)
        print('answer_count:', answer_count)
        
      
        url_list.append(url)
        print('-' * 20)
        # 存入数据库
        save_to_mongo(info)


# 连接到MongoDB
MONGO_URL = 'localhost'
MONGO_DB = 'zhihu_user_network'
MONGO_COLLECTION = 'users_info'
client = pymongo.MongoClient(MONGO_URL, port=27017)
db = client[MONGO_DB]


def save_to_mongo(info):
    # 保存到MongoDB中
    try:
        if db[MONGO_COLLECTION].insert(info):
            print('存储到 MongoDB 成功')
    except Exception:
        print('存储到 MongoDB 失败')


# url列表
url_list = []

if __name__ == '__main__':
    html = get_first_page()
    parse(html)
    for url in url_list:
        try:
            html_next = get_page(url)
            parse(html_next)
            time.sleep(2)
        except OSError:
            pass
        continue