# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 09:38:52 2018
@author: Administrator
对传入的APP数据进行初步清洗，以dataframe格式能读取的形式保存至相应目录
"""
import pandas as pd
import glob
import logging
import time
import datetime

start_time = time.time()
now_time = datetime.datetime.now()
raw_path = "../transfer/sms/sms_201806*"
output_path = "../SMS/"

logging.basicConfig(filename='log_sms.log',level=logging.INFO)

def clear_sms_main(file_path):
    with open(file_path) as f:
        data = f.readlines()
    list_all = []
    for one in data:
        l = one.split('|')
        if (len(l)==6) & ((len(l[0])==32) | (len(l[0])==64)) & ((len(l[3])==32) | (len(l[3])==64)) :
            l[5] = l[5][:-1]
            list_all.append(l)
    df = pd.DataFrame(list_all,columns=['phone_nm1','sms_type','mo_mt','phone_nm2','sms_time','sms_count'])
    output_file = "../SMS/%s.csv" % file_path[16:28]
    df.to_csv(output_file,index=None)
    logging.info("Cleared %s.  Length is %s" % (file_path[16:28],len(df)) )

if __name__ == "__main__":
    logging.info("\nNow time is %s. Clear file is %s. " % (now_time,raw_path) )
    files_path = glob.glob(raw_path)
    for one_path in files_path:
        clear_sms_main(one_path)
        
        
        
        
