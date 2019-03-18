# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 09:38:52 2018
@author: Administrator 
"""
import pandas as pd
import glob
import logging
import time
import datetime

start_time = time.time()
now_time = datetime.datetime.now()
raw_path = "../transfer/keyword/key_20181*"
output_path = "../Keyword/"

logging.basicConfig(filename='log_key.log',level=logging.INFO)

def clear_app_main(one_path):
    with open(one_path) as f:
        data = f.readlines()
    list_all = []
    for one in data:
        l = one.split('|')
        list_one = []
        if len(l) == 4:
            list_one.append(l[0])
            list_one.append(l[1])
            list_one.append(int(l[2]))
            list_one.append(int(l[3][0:9]))
            list_all.append(list_one)
    del data
    df = pd.DataFrame(list_all,columns=['phone_nm','app_name','app_count','app_time'])
    del list_all
    output_file = "../APP/%s.csv" % one_path[12:24]
    df.to_csv(output_file,index=None)
    logging.info("Cleared %s.  Length is %s" % (one_path[16:28],len(df)) )

if __name__ == "__main__":
    logging.info("Now time is %s. Clear file is %s. " % (now_time,raw_path) )
    files_path = glob.glob(raw_path)
    for one_path in files_path:
        clear_app_main(one_path)
        
        
        
        
