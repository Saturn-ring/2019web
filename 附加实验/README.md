# 爬虫：知乎用户信息

PB17061266 孙书情 https://github.com/Saturn-ring/2019web

### 1.完成情况：

1. 只完成了第一部分的一些，未实现第二部分。
2. 可以搜索出1000个用户的`userName,userLink,headline,sideItem,following_count,follower_count`但不能搜索出具体的following和follower的url，原因在于知乎的反爬虫。

### 2.代码思路：

2.  代码思路还是很简单的，根据一个种子用户，获取种子用户的follow者，然后再获取种子用户关注者的follow者，进而爬取1000个用户，但事实上，以我的代码思路如果要发现所有follower以及following的url，就不止是只爬取1000个数据了，应该是指数级的用户，因此在该lab中我只实现了调取关注着和被关注者的数量。

2. 主要应用了mongo数据库。

3. code部分共3个文件，其中有两个都是用于数据处理的，主要代码在scraw.py中:

   1. 我首先设置了访问知乎用户网页获取信息的http格式：

      `https://www.zhihu.com/api/v4/members/zhouyuan/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollowing_count%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20`

      可以看到我设置了对用户名，用户token等信息的询问，得到对应用户的有关信息，json格式，该json中的data部分是对于该用户每个follower的信息描述，也是我们进行迭代的关键。

   ```python
   def get_page(url):
       header = {
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/69.0.3497.12 Safari/537.36 '
       }
       response = requests.get(url, headers=header)
       return response.json()
   ```

   2. 对html中的json文件进行分析：数据存入mongo数据库zhihu_user_network中

      ```python
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
      ```

   3. 下面代码是mongo存入数据的小函数：

      ```python
      def save_to_mongo(info):
          # 保存到MongoDB中
          try:
              if db[MONGO_COLLECTION].insert(info):
                  print('存储到 MongoDB 成功')
          except Exception:
              print('存储到 MongoDB 失败')
      ```

   4. 主函数：设置了一个全局变量url列表 存储未访问的用户url，我们将每次调用parse（html)解析函数得到的follower的token信息加上预设值的http格式构成新的url存入列表中，以待被访问

      ```python
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
      ```

   5. 数据处理：database2csv.py是将数据库中的文件存入csv文件中，csv3json.py是将csv文件转成特定格式的json提交文件，在此不赘述其中的函数，可以直接看源码。

### 3.实验截图：

1. Ubuntu16.04 终端运行scrawl.py程序时输出的提示信息：

![屏幕快照 2020-01-04 下午9.02.49](figs/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202020-01-04%20%E4%B8%8B%E5%8D%889.02.49.png)
2. 最终的json文件形式：
![屏幕快照 2020-01-04 下午9.27.15](figs/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202020-01-04%20%E4%B8%8B%E5%8D%889.27.15.png)

### 4.实验总结：

​      由于临近期末，我只完成了该实验的一小部分，对于如何反爬虫并没有进行学习。根据我的思路可以通过构造链表的形式将每个用户对应的follower和following的url获取存储到数据库，但是我猜测如此频繁的访问知乎页面的api很可能会造成知乎对我的ip地址访问进行限制，仍旧绕不出要进行反爬虫的学习。