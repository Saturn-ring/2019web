# coding:utf-8
import requests
import re
import json
import pandas as pd
import csv
import os

path='./labdata/'
filename = path+'data.csv'
outputfile = path+'submit.json'
f=open(outputfile,'w+',encoding='utf-8')
writelist=[]
# 逐行读取csv文件
with open(filename,'r',encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row['name']
        link = row['url_token']
        headline = row['headline']
        following_count = row['following_count']
        follower_count = row['follower_count']
        sideItem = row['sideItem']
        rowdict = {'userName':name,'userLink':"https://www.zhihu.com/people/"+link,'headline':headline,'SideItem':sideItem,'followings':following_count,'followers':follower_count}
        writelist.append(rowdict)
json.dump(writelist,f,ensure_ascii=False)



