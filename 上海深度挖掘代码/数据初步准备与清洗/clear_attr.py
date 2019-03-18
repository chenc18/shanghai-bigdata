# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 09:38:52 2018
@author: Administrator
对传入的用户属性数据进行初步清洗，以dataframe格式能读取的形式保存至相应目录
"""
import pandas as pd
import glob
import logging
import time
import datetime

start_time = time.time()
now_time = datetime.datetime.now()
raw_path = "../transfer/attr/date*201807/*"
output_path = "../Attribute/attr201807.csv"

logging.basicConfig(filename='log_attr.log',level=logging.INFO)

headers = ['month_id','phone_nm','cust_type','user_num_6m','consume_type','jw_flag_12m',\
           'addr_name','sex','age','arpu','cert3','phone_brand','phone_type','innet_date','product_id',\
           'product_name','cust_level','acct_charge_6m','voice_cnt_1m','sms_cnt_1m','flux_cnt_1m','voice_cnt_6m','sms_cnt_6m',\
           'flux_cnt_6m','stop_sum_6m','pspt_num']

def clear_attr_main(file_path):
    attr_list = []
    with open(file_path) as f:
        data_all = f.readlines()
    logging.info("Raw data length is %s " % len(data_all) )
    for one_data in data_all:
#        one_list = one_data.split('|')
        one_list = one_data.split('\x01')
#        if len(one_list) == 27:
        if len(one_list) == 26:
#            one_list = ['nan' if (x==r'\N') or (x=='') else x for x in one_list]
            one_list = ['nan' if x==r'\N' else x for x in one_list]
#            one_list = one_list[0:26]
            one_list[25] = one_list[25][:-1]
            attr_list.append(one_list)
    df = pd.DataFrame(attr_list,columns=headers)
    df.to_csv(output_path ,index=None)
    logging.info("CLeared data length is %s" % len(df) )
    logging.info("Oneday data is cleared")
    
    
if __name__ == "__main__":
    logging.info("Now time is %s. Clear file is %s. " % (now_time,raw_path) )
    files_path = glob.glob(raw_path)
    for one_path in files_path:
        clear_attr_main(one_path)
        
        
        
        
