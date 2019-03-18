# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 13:41:43 2018
@author: Administrator
清洗位置数据
直接使用pandas读取，如果出错则输入出错的时间

"""
import pandas as pd		
import glob
import os
from multiprocessing import Pool
import logging

raw_path = "../transfer/loc/*"
processes_num = 12

logging.basicConfig(filename='log_loc.log',level=logging.INFO)

def clear_one(path1):
    days = path1[24:32]
    if not os.path.exists('../LOC/%s' % days):
        os.mkdir('../LOC/%s' % days)
    try:
        df = pd.read_csv(path1,sep='\t')
        df.columns = ["event_id","starttime","endtime","phone_nm","iemi","country_id","tag","lac","ci","q7"]
        df = df[["starttime","endtime","phone_nm","lac","ci"]]
        df.to_csv('../LOC/%s/%s.csv' % (days,path1[33:]), index=None,header=False)
    except:
        logging.info("出错%s" % path1)
#    os.remove(path1)
    
def clear_loc_main():
    files_path = glob.glob(raw_path)
    pool = Pool(processes = processes_num)
    for oneday_files_path in files_path:
        one_path = glob.glob("%s/*" % oneday_files_path)
        for path1 in one_path:
            pool.apply_async(clear_one, (path1,))
    pool.close()
    pool.join()
    


if __name__ == "__main__":
    clear_loc_main()


