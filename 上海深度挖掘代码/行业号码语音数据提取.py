#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 201901
@author: chencheng
提取与提供的行业号码用户语音来往过的所有电话号码。
"""
import pandas as pd
import glob
import logging
import os
import time
from multiprocessing import Pool

logging.basicConfig(filename="log_filter_call.log",level=logging.INFO)
start_time = time.time()

#进程数量
process_num = 20

output_file = "/data1/machine_learning01/call/"
#读取加密后导入系统的文件
df_out_data = pd.read_csv("phone_nm_out.csv", sep=',', names=["phone","phone_nm_out"])

def filter_one(file_path):
    logging.info("Filter call %s" % file_path)
    df_all = pd.read_csv(file_path)
    df = df_all[(df_all.phone_nm1.isin(df_out_data.phone_nm_out.tolist()))|(df_all.phone_nm2.isin(df_out_data.phone_nm_out.tolist()))]
    df.to_csv(os.path.join(output_file, file_path[12:]), index=None)
    logging.info("%s is cleared . Length is %s" % (file_path, len(df)) )
    

def filter_call_main():
    file_paths = glob.glob("/data1/CALL/call_2018*.csv")
    pool = Pool(processes = process_num)
    for file_path in file_paths:
        pool.apply_async(filter_one,(file_path,))
    pool.close()
    pool.join()

def concat_phone():
    files_path = glob.glob("/data1/machine_learning01/call/call*.csv")
    phone_list = []
    for file_path in files_path:
        df = pd.read_csv(file_path)
        phone_list.append(df.phone_nm1.tolist())
        phone_list.append(df.phone_nm2.tolist())
        phone_list = list(set(phone_list))
    df_phone = pd.DataFrame(phone_list,columns=['phone_nm'])
    df_phone.to_csv("/data1/machine_learning01/yy_phone_all.csv",index=None)
        


if __name__ == "__main__":
    logging.info("Start filter call.")
    filter_call_main()

