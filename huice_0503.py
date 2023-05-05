#coding=utf-8
#import baostock as bs
import pandas as pd
import talib
import requests
import random
from hyper.contrib import HTTP20Adapter
import time, datetime
import json
import logging
#import code_dict
import math






logging.basicConfig(level=logging.INFO, format="%(message)s", filename="./huice0503.log", filemode="a")

user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29",
                   "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
                   'Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)', 'Mozilla/5.0 (compatible; U; ABrowse 0.6;  Syllable) AppleWebKit/420+ (KHTML, like Gecko)', 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)', 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR   3.5.30729)', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0;   Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;   SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; Acoo Browser; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; Avant Browser)', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1;   .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Maxthon; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)', 'Mozilla/4.0 (compatible; Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729); Windows NT 5.1; Trident/4.0)', 'Mozilla/4.0 (compatible; Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727); Windows NT 5.1; Trident/4.0; Maxthon; .NET CLR 2.0.50727; .NET CLR 1.1.4322; InfoPath.2)',
                   'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB6; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)']

headers_1 = {"user-agent": random.choice(user_agent_list),}

headers = {':authority': 'stock.xueqiu.com',
           ':method': 'GET',
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'accept-encoding': 'gzip, deflate, br',
           'accept-language': 'zh-CN,zh;q=0.9',
           'cache-control': 'max-age=0',
           'cookie': 'device_id=04df9bee31d96920289fbec1a4e1e03a; s=cf122uuhnb; bid=1fa9bc3995022e7a50364963f5000816_l7bkxqzb; xq_is_login=1; Hm_lvt_1db88642e346389874251b5a1eded6e3=1681089228; cookiesu=321682385111462; xq_a_token=f704e2235248250ea622aff278faa3ad2dcf5c17; xqat=f704e2235248250ea622aff278faa3ad2dcf5c17; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjY0ODQ2ODUzODUsImlzcyI6InVjIiwiZXhwIjoxNjg0OTgwNDE1LCJjdG0iOjE2ODIzODg0MTU5NTMsImNpZCI6ImQ5ZDBuNEFadXAifQ.atGhlm10Wgt-wNq7VCPKgzIQMd5RaFH65lPDf10YM9-cTt5crS3igFP0iRPb-I2hLRK3i9xoVqubE3IXAllG8dq_SYgetImaBWnnHRJBctwCX_4U30Zh6YrL2VFImzkCijWNBtMs_jBHJRBMbebMR6KiGlYAyiMl4RaPVjwOSFcWZ6jDYmnvEq4eV7ag74pVp1PNMqg5Spsawop_aI8x6Lj2GztkTJbhfqTWeQp-0PpeaKY3ZqKRAFvyJ3lqGr6GhcwFMkJR8eExaJLwYqMjAELaRhMl0Olun4Jxa_5dVYn5nLEWUGXqBPeh_gTXjXEsxxdBTfhVRTF_oXjimMJikw; xq_r_token=d52281f19ef5362552e86820e063c625a03ffb8a; u=6484685385; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1682388492',
           'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
           'sec-ch-ua-mobile': '?0',
           'sec-ch-ua-platform': '"Windows"',
           'sec-fetch-dest': 'document',
           'sec-fetch-mode': 'navigate',
           'sec-fetch-site': 'none',
           'sec-fetch-user': '?1',
           'upgrade-insecure-requests': '1',
           "user-agent": random.choice(user_agent_list),
}


headers_1 = {#':authority': 'stock.xueqiu.com',
           #':method': 'GET',
           #':path': code_name_list_url,
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'accept-encoding': 'gzip, deflate, br',
           'accept-language': 'zh-CN,zh;q=0.9',
           'cache-control': 'max-age=0',
           'cookie': 'device_id=04df9bee31d96920289fbec1a4e1e03a; s=cf122uuhnb; bid=1fa9bc3995022e7a50364963f5000816_l7bkxqzb; xq_is_login=1; Hm_lvt_1db88642e346389874251b5a1eded6e3=1681089228; cookiesu=321682385111462; xq_a_token=f704e2235248250ea622aff278faa3ad2dcf5c17; xqat=f704e2235248250ea622aff278faa3ad2dcf5c17; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjY0ODQ2ODUzODUsImlzcyI6InVjIiwiZXhwIjoxNjg0OTgwNDE1LCJjdG0iOjE2ODIzODg0MTU5NTMsImNpZCI6ImQ5ZDBuNEFadXAifQ.atGhlm10Wgt-wNq7VCPKgzIQMd5RaFH65lPDf10YM9-cTt5crS3igFP0iRPb-I2hLRK3i9xoVqubE3IXAllG8dq_SYgetImaBWnnHRJBctwCX_4U30Zh6YrL2VFImzkCijWNBtMs_jBHJRBMbebMR6KiGlYAyiMl4RaPVjwOSFcWZ6jDYmnvEq4eV7ag74pVp1PNMqg5Spsawop_aI8x6Lj2GztkTJbhfqTWeQp-0PpeaKY3ZqKRAFvyJ3lqGr6GhcwFMkJR8eExaJLwYqMjAELaRhMl0Olun4Jxa_5dVYn5nLEWUGXqBPeh_gTXjXEsxxdBTfhVRTF_oXjimMJikw; xq_r_token=d52281f19ef5362552e86820e063c625a03ffb8a; u=6484685385; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1682388492',
           'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
           'sec-ch-ua-mobile': '?0',
           'sec-ch-ua-platform': '"Windows"',
           'sec-fetch-dest': 'document',
           'sec-fetch-mode': 'navigate',
           'sec-fetch-site': 'none',
           'sec-fetch-user': '?1',
           'upgrade-insecure-requests': '1',
           "user-agent": random.choice(user_agent_list),
}


format_string="%Y-%m-%d %H:%M:%S"




#就算数据帧
def get_data_df(url):
    sessions = requests.session()
    sessions.mount(url, HTTP20Adapter())
    res = sessions.get(url, headers=headers)
    #res = requests.get(url=url, headers=headers).json()
    data_list_1 = []
    data_list = res.json().get("data").get("item")
    if not data_list:
        return None
    for data in data_list:
        tre_timeArray = time.localtime((data[0] + 13*3600*1000)/1000)
        tre_otherStyleTime = time.strftime("%Y-%m-%d", tre_timeArray)
        data[0] = str(tre_otherStyleTime)
        data_list_1.append(data)
    df = pd.DataFrame(data_list_1).drop([6, 10, 11], axis=1)
    df = df.rename(columns={0: 'day', 1: 'liang', 2: 'open', 3: 'high', 4: 'low', 5: 'close', 7: 'zhang_fu', 8: 'huan_shou', 9: 'cheng_jiao_e'})
    #print(df)
    df[['open', 'close', 'low', 'high','zhang_fu', 'cheng_jiao_e', 'huan_shou']] = df[['open', 'close', 'low', 'high', 'zhang_fu', 'cheng_jiao_e', 'huan_shou']].astype('float64')
    df[['liang']] = df[['liang']].astype('int64')
    df.index = pd.DatetimeIndex(df['day'])
    #df.set_index('datetime')
    return df


def calc_zb(df):
#计算日线kdj
    df['K'], df['D'] = talib.STOCH(df['high'].values,
                                           df['low'].values,
                                           df['close'].values,
                                           fastk_period=9,
                                           slowk_period=5,
                                           slowk_matype=1,
                                           slowd_period=5,
                                           slowd_matype=1)

    df.loc[:, 'J'] = 3.0 * df.loc[:, 'K'] - 2.0 * df.loc[:, 'D']
    #计算均线
    df['ma5'] = talib.SMA(df['close'],timeperiod=5)
    df['ma10'] = talib.SMA(df['close'],timeperiod=10)
    df['ma20'] = talib.SMA(df['close'],timeperiod=20)
    df['ma30'] = talib.SMA(df['close'],timeperiod=30)
    df['ma60'] = talib.SMA(df['close'],timeperiod=60)
    #df['ma120'] = talib.SMA(df['close'],timeperiod=120)
    df['ma250'] = talib.SMA(df['close'],timeperiod=250)
    df['vol5'] = talib.MA(df['liang'],timeperiod=5, matype=0)
    df['vol10'] = talib.MA(df['liang'],timeperiod=10, matype=0)
    #计算macd
    df['dif'], df['dea'], df['bar'] = talib.MACD(df['close'].values, fastperiod=12, slowperiod=26, signalperiod=9)
    return df



dtime = datetime.datetime.now()

u_time = (time.mktime(dtime.timetuple()) + 12 * 3600) * 1000
timestamp = str(u_time).split(".")[0]
print(timestamp)



url =  'http://98.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112402803120599104636_1675409984210&pn=1&pz=3500&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=|0|0|0|web&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1675409984211'

res = requests.get(url=url)
yyx_str = res.text.split('data":')[1].split("})")[0]
#print(yyx_str)
yyx_json = json.loads(yyx_str)
#print(yyx_json)
data = yyx_json.get("diff")
code_list = []
for i in  data:
    #print(i.get("f12")[:2])
    #if "00" == i.get("f12")[:2] and "ST" not in i.get("f14"):
    if i.get("f12")[:2] in ["60", "00"] and "ST" not in i.get("f14") and "-" !=  i.get("f10") and "-" != i.get("f3") and i.get("f12"):
        #print(i.get("f14"))
        name = i.get("f14")
        code = 'SZ' + i.get("f12") if "00" == i.get("f12")[:2] else 'SH' + i.get("f12")
        zhang_fu = i.get("f3")
        huan_shou = i.get("f8")
        cheng_jiao_e = i.get("f6")/100000000
        dang_qian_jia = i.get("f2")
        zui_di_jia = i.get("f16")
        zui_gao_jia = i.get("f15")
        kai_pan_jia = i.get("f17")
        pe = i.get("f9")
        shang_ying_xian = (i.get("f15") - i.get("f2"))/i.get("f2")

        if code:
            #code = 'SZ' + code if "00" == code[:2] else 'SH' + code
            #print(day_df)
                #today_data = day_df.iloc[-1].to_dict()
                #cheng_jiao_e = today_data.get('cheng_jiao_e')/100000000
                #high = today_data.get('high')
                #dang_qian_jia = today_data.get('close')
                #kai_pan_jia = today_data.get('open')
                #shang_ying_xian = (high - dang_qian_jia)/dang_qian_jia
             
            if 3 < zhang_fu < 6 and cheng_jiao_e > 1 and dang_qian_jia > kai_pan_jia and shang_ying_xian < 0.05 and huan_shou < 10:
                day_url = "https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol={0}&begin={1}&period=day&type=before&count=-300&indicator=kline".format(code, timestamp)
                print(day_url)
                day_df = get_data_df(day_url)
                if day_df is not None:
                    #print(11111)
                    week_url = "https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol={0}&begin={1}&period=week&type=before&count=-300&indicator=kline".format(code, timestamp)
                    week_df = get_data_df(week_url)
                    day_df = calc_zb(day_df)
                    #print(day_df.iloc[-1].to_dict())
                    today_data = day_df.iloc[-1].to_dict()
                    today_liang = today_data.get('liang')
                    low = today_data.get('low')
                    high = today_data.get('high')
                    close = today_data.get('close')
                    yesterday_data = day_df.iloc[-2].to_dict()
                    yes_close = yesterday_data.get('close')
                    yesterday_3_data = day_df.iloc[-3].to_dict()
                    shiti_high_10_list = []
                    for index in range(-10,-1):
                        data_dict = day_df.iloc[index].to_dict()
                        tmp_open = data_dict.get("open")
                        tmp_high = data_dict.get("high")
                        tmp_close = data_dict.get("close")
                        tmp_list = [tmp_open, tmp_high, tmp_close]
                        tmp_list.sort(reverse=True)
                        #print(tmp_list)
                        shiti_high_10_list.append(tmp_list[1])
                   
                    shiti_high_11_list = []
                    low = today_data.get('low')
                    high = today_data.get('high')
                    close = today_data.get('close')
                    for index in range(-11,-2):
                        data_dict = day_df.iloc[index].to_dict()
                        tmp_open = data_dict.get("open")
                        tmp_high = data_dict.get("high")
                        tmp_close = data_dict.get("close")
                        tmp_list = [tmp_open, tmp_high, tmp_close]
                        tmp_list.sort(reverse=True)
                        #print(tmp_list)
                        shiti_high_11_list.append(tmp_list[1])
                    ya_li_1 = (yes_close - max(shiti_high_11_list))/max(shiti_high_11_list) * 100
                    
                    liang_max_5days = 0
                    for idx in range(-5,-1):
                        data_dict = day_df.iloc[idx].to_dict()
                        tmp_liang = data_dict.get("liang")
                        if tmp_liang > liang_max_5days:
                            liang_max_5days = tmp_liang
                    #print(shiti_high_10_list)
                    ya_li = (close - max(shiti_high_10_list))/max(shiti_high_10_list) * 100
                    yes_3_liang = yesterday_3_data.get('liang')
                    ma5 = today_data.get('ma5')
                    ma10 = today_data.get('ma10')
                    ma20 = today_data.get('ma20')
                    ma30 = today_data.get('ma30')
                    ma60 = today_data.get('ma60')
                    #ma120 = today_data.get('ma120')
                    ma250 = today_data.get('ma250')
                    ma5_distance = (low - ma5)/ma5 * 100
                    yesterday_liang = yesterday_data.get('liang')
                    fang_liang = today_liang / yesterday_liang
                    day_mavol5 = today_data.get('vol5')
                    day_mavol10 = today_data.get('vol10')
                    day_macd = today_data.get("bar") * 2
                    to_day_j = today_data.get("J")
                    to_day_k = today_data.get("K")
                    to_day_d = today_data.get("D")
                    ma_data_list = []
                    for k,v in today_data.items():
                        if "ma" in k:
                            if v > -99999:
                                if 'ma250' != k:
                                    ma_data_list.append(v)

                    week_df = calc_zb(week_df)
                    #print(week_df.iloc[-1].to_dict())
                    toweek_data = week_df.iloc[-1].to_dict()
                    week_macd = toweek_data.get("bar") * 2
                    to_week_j = toweek_data.get("J")
                    to_week_k = toweek_data.get("K")
                    to_week_d = toweek_data.get("D")
                    week_ma_data_list = []
                    week_ma_250 = 0
                    for k,v in toweek_data.items():
                        if "ma" in k:
                            #print(type(v))
                            if v > -99999:
                                if 'ma250' == k:
                                    week_ma_250 = v
                                week_ma_data_list.append(v)

                    #print(ma_data_list, week_ma_data_list)
                    try:
                        max_ma = max(ma_data_list)
                        week_max_ma = max(week_ma_data_list)
                        if week_ma_250 == week_max_ma:
                            week_ma_data_list.remove(week_ma_250)
                            week_max_ma = max(week_ma_data_list)
                    except Exception as e:
                        week_max_ma = 0
                    
                    #print(ya_li, dang_qian_jia, max_ma, week_max_ma, ma5_distance, day_mavol5, day_mavol10, ma5, ma10, ma20, ma30, ma60, ma250)
                    if dang_qian_jia > max_ma and ya_li > 0.5 and ya_li_1 < 0.5 and fang_liang > 1.2 and today_liang > liang_max_5days and dang_qian_jia >= week_max_ma and ma5_distance < 1 and day_mavol5 > day_mavol10 and ma5 > ma10 > ma20 > ma30 > ma60:
                        jun_xian_distance = (ma5 - ma60)/ma60 * 100
                        print(2222222222, name, jun_xian_distance)
                        #print(day_macd, week_macd)
                        if 1 > day_macd > 0 and jun_xian_distance < 10:# and week_macd > 0:
                            #print(to_day_j, to_day_k, to_day_d, to_week_j,to_week_k, to_week_d)
                          
                            if (100 > to_day_j and to_day_d < 80):# and (100 > to_week_j > to_week_k > to_week_d and to_week_d < 80):
                                #print(3333333333)
                                gai_nian_url = "http://stockpage.10jqka.com.cn/{0}/".format(code[2:])
                                gai_nian = requests.get(gai_nian_url, headers=headers_1).text.split('dd title="')[1].split('">')[0]
                                logging.info(str(dtime).split()[0] + "-->" + str(name) + " ($题材概念: " + gai_nian)
                                #logging.info(day.split()[0] + "-->" + str(name))
