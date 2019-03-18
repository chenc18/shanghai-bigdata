# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 17:45:49 2019
@author: chencheng
（每隔一个小时）首先循环获取需要爬取的微博，根据id去数据库匹配，如果没有则保存到数据库
（每十分钟）从数据库读取需要爬取的微博链接，然后去分别获取每一个的具体数据
分两个数据表，一个表存微博id，一个存具体数据
时间通过当前时间的整数来控制
获取具体微博内容时考虑增加分布式爬虫或者更改为scrapy
"""
import pandas as pd
from bs4 import BeautifulSoup
import json
import os
import re
from urllib import request
import datetime
import time
import logging

logging.basicConfig(filename='log.log',level=logging.INFO)
head = {}
head['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
output_files1 = 'weibo.csv'
output_content = 'weibo_content.csv'

#获取发布时间
def get_create_time(now_time,created_at):
    try:
        times = get_now_time(now_time)
        if created_at == "刚刚":
            return times 
        if '分钟' in created_at:
            minute = str(int(times[10:12]) - int(created_at.split('分')[0]) )
            if len(minute) == 1:
                minute = '0' + minute
            create_time = times[:10] + minute
            return create_time
        else:
            return created_at
    except:
        return created_at
    
#获取当前时间，精确到分
def get_now_time(now_time):
    month = str(now_time.month)
    day = str(now_time.day)
    hours = str(now_time.hour)
    minute = str(now_time.minute)
    if len(month) == 1:
        month = '0' + month
    if len(day) == 1:
        day = '0' + day
    if len(hours) == 1:
        hours = '0' + hours
    if len(minute) == 1:
        minute = '0' + minute
    return str(now_time.year) + month + day + hours + minute

#循环获取需要爬取的微博主ID，将近期发布的微博保存至数据库。
def get_all_weibo(now_time,url):
    req = request.Request(url,headers = head)
    response = request.urlopen(req)
    html = response.read()
    data_json = json.loads(html)
    data_all = data_json["data"]["cards"]
    data = []
    for i in range(len(data_all)):
        try:
            one_list = []
            data_one = data_all[i]
            one_list.append(data_one['itemid'])
            one_list.append(data_one['scheme'])
            created_at = data_one['mblog']['created_at']
            created_at = get_create_time(now_time,created_at)
            one_list.append(created_at)  
            data.append(one_list)
        except:
            continue
    headers = ["id","url","time"]
    df = pd.DataFrame(data,columns=headers)
    df['content'] = 0
    if os.path.exists(output_files1): 
        df_old = pd.read_csv(output_files1)
        df_new = df[~df.id.isin(df_old.id.tolist())]
        df = pd.concat([df_new,df_old])
        df = df.drop_duplicates(subset=['id'])
    df.to_csv(output_files1,index=None,encoding='utf-8')

#获取具体微博的数据。从数据库中获取数据，如果文本内容为空则保存，不为空则不保存。
def get_content(now_time):
    logging.info('Began to crawl individual micro blog specific content.')
    df_weibo = pd.read_csv(output_files1)
    all_list = []
    for i in range(len(df_weibo)):
        try:
            url_id = re.findall(r'mblogid=(.*?)&luicode',df_weibo.iloc[i][1])[0]
            url = 'https://m.weibo.cn/statuses/show?id=%s' % url_id
            req = request.Request(url,headers = head)
            response = request.urlopen(req)
            html = response.read()
            data_json = json.loads(html)
            content = data_json['data']['text']
            if df_weibo.iloc[i][3] == 0:
                df_weibo.iloc[i,3] = content
                df_weibo.to_csv(output_files1,index=None,encoding='utf-8')
                logging.info('Obtain and save microblog content')
            reposts_count = data_json['data']['reposts_count']
            comments_count = data_json['data']['comments_count']
            attitudes_count = data_json['data']['attitudes_count']
            now_times = get_now_time(now_time)
            one_list = []
            one_list.append(now_times)
            one_list.append(df_weibo.iloc[i][0])
            one_list.append(reposts_count)
            one_list.append(comments_count)
            one_list.append(attitudes_count)
            all_list.append(one_list)
        except:
            logging.info('----Faild----  weibo content ')
            continue
    headers = ["get_time","id_one","reposts_count","comments_count","attitudes_count"]
    df = pd.DataFrame(all_list,columns=headers) 
    if os.path.exists(output_content): 
        df_old = pd.read_csv(output_content)
        df = pd.concat([df,df_old])
    df.to_csv(output_content,index=None,encoding='utf-8') 
    

if __name__ == "__main__":
    now_time = datetime.datetime.now()
    url_all = ['https://m.weibo.cn/api/container/getIndex?uid=5737325620&luicode=10000011&lfid=100103type%3D1%26q%3DJeffrey%E8%91%A3%E5%8F%88%E9%9C%96&type=uid&value=5737325620&containerid=1076035737325620','https://m.weibo.cn/api/container/getIndex?uid=1797279194&luicode=10000011&lfid=100103type%3D1%26q%3D%E9%93%82%E7%88%B5%E6%97%85%E6%8B%8D&type=uid&value=1797279194&containerid=1076031797279194','https://m.weibo.cn/api/container/getIndex?uid=1252397723&luicode=10000011&lfid=100103type%3D1%26q%3Dcucn201%E7%99%BD%E5%AE%A2&type=uid&value=1252397723&containerid=1076031252397723','https://m.weibo.cn/api/container/getIndex?uid=3216200194&luicode=10000011&lfid=100103type%3D1%26q%3D%E5%94%AF%E4%B8%80%E8%A7%86%E8%A7%89%E5%85%A8%E7%90%83%E6%97%85%E6%8B%8D%E6%80%BB%E7%AB%99&type=uid&value=3216200194&containerid=1076033216200194']
    for i in range(len(url_all)):
        url = url_all[i]
        try:
            get_all_weibo(now_time,url)
        except:
            continue
    logging.info('微博获取完毕，开始获取详情')
    get_content(now_time)

#Jeffrey董又霖。  cucn201白客  铂爵旅拍   唯一视觉全球旅拍总站
#Jeffrey董又霖      https://m.weibo.cn/api/container/getIndex?uid=5737325620&luicode=10000011&lfid=100103type%3D1%26q%3DJeffrey%E8%91%A3%E5%8F%88%E9%9C%96&type=uid&value=5737325620&containerid=1076035737325620
#铂爵旅拍           https://m.weibo.cn/api/container/getIndex?uid=1797279194&luicode=10000011&lfid=100103type%3D1%26q%3D%E9%93%82%E7%88%B5%E6%97%85%E6%8B%8D&type=uid&value=1797279194&containerid=1076031797279194
#cucn201白客       https://m.weibo.cn/api/container/getIndex?uid=1252397723&luicode=10000011&lfid=100103type%3D1%26q%3Dcucn201%E7%99%BD%E5%AE%A2&type=uid&value=1252397723&containerid=1076031252397723
#唯一视觉全球旅拍总站 https://m.weibo.cn/api/container/getIndex?uid=3216200194&luicode=10000011&lfid=100103type%3D1%26q%3D%E5%94%AF%E4%B8%80%E8%A7%86%E8%A7%89%E5%85%A8%E7%90%83%E6%97%85%E6%8B%8D%E6%80%BB%E7%AB%99&type=uid&value=3216200194&containerid=1076033216200194
    
    
