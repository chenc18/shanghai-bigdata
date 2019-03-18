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
raw_path = "../transfer/call/*20181*"
output_path = "../CALL/call_"

logging.basicConfig(filename='log_call.log',level=logging.INFO)

#语音数据
def clear_one(file_path):
    with open(file_path) as f:
        data = f.readlines()
    all_list = []
    for one in data:
        l = one.split('\t')
        list_one = []
        try:
            if ((len(l[2])==32) | (len(l[2])==64)) & ((len(l[3])==32) | (len(l[3])==64)) & ((l[1]=="主叫") | (l[1]=="被叫")):
                list_one.append(l[2])
                list_one.append(l[3])
                list_one.append(l[1])
                list_one.append(int(l[4]))
                list_one.append((l[5]))
                all_list.append(list_one)
        except:
            continue
    delete_count = len(data) - len(all_list)
    df = pd.DataFrame(all_list,columns=['phone_nm1','phone_nm2','call_type','call_start_time','call_duration'])
    return df,delete_count

def clear_call_main(file_path):
    day = file_path[25:33]
    day_paths = glob.glob('%s/*' % file_path)
    df_list = []
    delete_all = 0
    for one_path in day_paths:
        df_one,delete_one = clear_one(one_path)
        delete_all = delete_all + delete_one
        df_list.append(df_one)
    df = pd.concat(df_list)
    df.to_csv('../CALL/%s.csv' % day, index=None)
    logging.info("Cleared %s.  Length is %s" % (day,len(df)) )

if __name__ == "__main__":
    logging.info("Now time is %s. Clear file is %s. " % (now_time,raw_path) )
    files_path = glob.glob(raw_path)
    for one_path in files_path:
        clear_call_main(one_path)
        
        
        
        
