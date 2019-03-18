#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 201901
@author: chencheng
提取与行业号码沟通过的用户的常用数据
"""
import pandas as pd
import glob
import os
from multiprocessing import Pool


processes_num = 15
df_call_phone = pd.read_csv("/data1/machine_learning01/yy_phone_all.csv", names=["phone_nm"])
phone = df_call_phone.phone_nm.tolist()


#提取当前号码app使用情况
def get_app_one(app_path):
    df = pd.read_csv(app_path)
    df = df[df.phone_nm.isin(phone)]
    df.to_csv('app/%s' % app_path[11:], index=None)
def get_app():
    files_path = glob.glob("/data1/APP/app_2018*.csv")
    pool = Pool(processes = processes_num)
    for app_path in files_path:
        pool.apply_async(get_app_one,(app_path,))
    pool.close()
    pool.join()
    print("APP提取完毕")
    

#提取关键词
def get_keyword_one(key_path):
    df = pd.read_csv(key_path)
    df = df[df.phone_nm.isin(phone)]
    df.to_csv('keyword/%s' % key_path[15:], index=None)
def get_keyword():
    files_path = glob.glob("/data1/Keyword/key_2018*.csv")
    pool = Pool(processes = processes_num)
    for key_path in files_path:
        pool.apply_async(get_keyword_one,(key_path,))
    pool.close()
    pool.join()
    print("关键词提取完毕")
    

    
#提取所有语音
def get_call_one(call_path):
    df = pd.read_csv(call_path)
    df = df[(df.phone_nm1.isin(phone))|(df.phone_nm2.isin(phone))]
    df.to_csv('call/%s' % call_path[12:], index=None)
def get_call():
    files_path = glob.glob("/data1/CALL/call_2018*.csv")
    pool = Pool(processes = processes_num)
    for call_path in files_path:
        pool.apply_async(get_call_one,(call_path,))
    pool.close()
    pool.join()
    print("语音提取完毕")
    

if __name__ == "__main__":
    get_app()
    get_call()
    get_keyword()

