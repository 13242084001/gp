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
import code_dict
import math








logging.basicConfig(level=logging.INFO, format="%(message)s", filename="./xuangegu.log", filemode="a")

user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29",
                   "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
                   'Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)', 'Mozilla/5.0 (compatible; U; ABrowse 0.6;  Syllable) AppleWebKit/420+ (KHTML, like Gecko)', 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)', 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR   3.5.30729)', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0;   Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;   SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; Acoo Browser; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; Avant Browser)', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1;   .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Maxthon; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)', 'Mozilla/4.0 (compatible; Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729); Windows NT 5.1; Trident/4.0)', 'Mozilla/4.0 (compatible; Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727); Windows NT 5.1; Trident/4.0; Maxthon; .NET CLR 2.0.50727; .NET CLR 1.1.4322; InfoPath.2)',
                   'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB6; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)']

headers_1 = {"user-agent": random.choice(user_agent_list),}

headers = {#':authority': 'stock.xueqiu.com',
           #':method': 'GET',
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'accept-encoding': 'gzip, deflate, br',
           'accept-language': 'zh-CN,zh;q=0.9',
           'cache-control': 'max-age=0',
           'cookie': 'device_id=8c6a1a588fd3875dda55ef4ad15de38b; Hm_lvt_1db88642e346389874251b5a1eded6e3=1683687625; xq_a_token=5a5afbeefee214b96a47722a3586a7cde5b6297e; xqat=5a5afbeefee214b96a47722a3586a7cde5b6297e; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjY0ODQ2ODUzODUsImlzcyI6InVjIiwiZXhwIjoxNjg2Mjc5NjIxLCJjdG0iOjE2ODM2ODk3NTAxMzMsImNpZCI6ImQ5ZDBuNEFadXAifQ.dDZK-BwPEGBRj4XoAbLVVo5-ld-1dHFnu96Fj_EfUbisLCvW16e96hfxifZP7E6Q9ThaNEx9gD20dicTrh6lvYQ0_LQPL1JWPjja-Td0PSTy7vG8GlM1zuGpc2CBHp33c8oelTgjJgqNFt463VVZKRHR-AGEo_cWnytiKgVvi9XgZKFsGS722gXgNWQ0jXkk1m5CTknJun6UMIym1fYfFGvot0dqk7rfsUgrl-RDAj65IpCNuNXXwC6chwWX1PCQhsUcAN_NDcH6-diAXsV162D_Wdv7mfGKKodFzrJaZYisP76QjjS36q5dzVDKyeiKTItp0iDC0Z2tNdtwwshh5w; xq_r_token=d8f01b8094dfc86b89fe3ffd089b8a4037eb6c6e; xq_is_login=1; u=6484685385; is_overseas=0; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1683689819',
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
def get_data_df(url, isweek=0):
    sessions = requests.session()
    sessions.mount(url, HTTP20Adapter())
    res = sessions.get(url, headers=headers, timeout=20)
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
    if isweek:
        week_last_day = data_list[-1][0]
        #print(week_last_day)
        if week_last_day != day:
            days = day_list[day_list.index(week_last_day) + 1: day_list.index(day.split(" ")[0])+1]
            print(days)
            
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

url = "http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=sz000002&scale=240&ma=5&datalen=60"
day_list = []
res = requests.get(url=url)
for li in res.json():
    day = li.get("day")[:10]
    if day not in day_list:
        day_list.append(day)
print(day_list)

all_data_dict = {}
for code, name in code_dict.code_dict.items():
    if code[:2] in ["60", "00"]:
        code = 'SZ' + code if "00" == code[:2] else 'SH' + code
        day_url = "https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol={0}&begin={1}&period=day&type=before&count=-300&indicator=kline".format(
            code, timestamp)
        
        print(day_url)
        day_df = get_data_df(day_url)
        if day_df is not None:
            day_df = calc_zb(day_df)
            all_data_dict[code] = [day_df, name]
for day in day_list[-50:]:
    idx = -(len(day_list) - day_list.index(day))
    for code, df_list in all_data_dict.items():
        today_data = df_list[0].iloc[idx].to_dict()
        
        yesterday_data = df_list[0].iloc[idx-1].to_dict()
        low = today_data.get('low')

        cheng_jiao_e = today_data.get('cheng_jiao_e')/10000000
        high = today_data.get('high')
        dang_qian_jia = today_data.get('close')
        kai_pan_jia = today_data.get('open')
        shang_ying_xian = (high - dang_qian_jia)/dang_qian_jia
        zhang_fu = today_data.get('zhang_fu')
        huan_shou = today_data.get('huan_shou')


        if 1.5 < zhang_fu < 6 and cheng_jiao_e > 0.6 and dang_qian_jia > kai_pan_jia and shang_ying_xian < 0.05 and huan_shou < 10:
            today_liang = today_data.get('liang')
            ma5 = today_data.get('ma5')
            ma10 = today_data.get('ma10')
            ma5_distance = (low - ma5) / ma5 * 100
            day_mavol5 = today_data.get('vol5')
            day_mavol10 = today_data.get('vol10')
            if day_mavol5 > day_mavol10 and ma5_distance < 1 and round(ma5, 7) >= round(ma10, 7):
                high = today_data.get('high')
                close = today_data.get('close')
                yesterday_liang = yesterday_data.get('liang')
                fang_liang = today_liang / yesterday_liang
                if fang_liang > 1.2:
                    yes_close = yesterday_data.get('close')
                    #yesterday_3_data = day_df.iloc[-3].to_dict()
                    shiti_high_10_list = []
                    for index in range(idx-10,idx):
                        data_dict = df_list[0].iloc[index].to_dict()
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
                    for index in range(idx-11,idx-1):
                        data_dict = df_list[0].iloc[index].to_dict()
                        tmp_open = data_dict.get("open")
                        tmp_high = data_dict.get("high")
                        tmp_close = data_dict.get("close")
                        tmp_list = [tmp_open, tmp_high, tmp_close]
                        tmp_list.sort(reverse=True)
                        #print(tmp_list)
                        shiti_high_11_list.append(tmp_list[1])
                    ya_li_1 = (yes_close - max(shiti_high_11_list))/max(shiti_high_11_list) * 100
                    ya_li = (close - max(shiti_high_10_list)) / max(shiti_high_10_list) * 100
                    if ya_li_1 < 0.5 and ya_li > 0.5:

                        liang_max_5days = 0
                        for idxx in range(idx-5,idx):
                            data_dict = df_list[0].iloc[idxx].to_dict()
                            tmp_liang = data_dict.get("liang")
                            if tmp_liang > liang_max_5days:
                                liang_max_5days = tmp_liang
                        #print(shiti_high_10_list)
                        if today_liang > liang_max_5days:
                            #yes_3_liang = yesterday_3_data.get('liang')

                            ma20 = today_data.get('ma20')
                            ma30 = today_data.get('ma30')
                            ma60 = today_data.get('ma60')
                            ma250 = today_data.get('ma250')
                            yes_ma5 = yesterday_data.get('ma5')
                            yes_ma10 = yesterday_data.get('ma10')
                            yes_ma20 = yesterday_data.get('ma20')
                            yes_ma30 = yesterday_data.get('ma30')
                            yes_ma60 = yesterday_data.get('ma60')
                            atan5 = math.atan((ma5/yes_ma5 - 1)*100) * 180 / 3.1416
                            atan10 = math.atan((ma10/yes_ma10 - 1)*100) * 180 / 3.1416
                            atan20 = math.atan((ma20/yes_ma20 - 1)*100) * 180 / 3.1416
                            atan30 = math.atan((ma30/yes_ma30 - 1)*100) * 180 / 3.1416
                            atan60 = math.atan((ma60/yes_ma60 - 1)*100) * 180 / 3.1416
                            atan_len = 0
                            for atan in [atan5, atan10, atan20, atan30, atan60]:
                                if atan > 10:
                                    atan_len += 1
                            #print(atan5, atan10, atan20,atan30,atan60)
                            if atan_len >=3 and min(atan5, atan10, atan20) > 10:
                                day_macd = today_data.get("bar") * 2
                                to_day_j = today_data.get("J")
                                to_day_k = today_data.get("K")
                                to_day_d = today_data.get("D")
                                ma_data_list = []
                                for k,v in today_data.items():
                                    if "ma" in k:
                                        if v > -99999:
                                            #if 'ma250' != k:
                                            ma_data_list.append(v)
                                print(day)
                                day += " 8:00:00"
                                time_array = time.strptime(day, format_string)
                                timestamp = str(int(time.mktime(time_array)) * 1000)
                                week_url = "https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol={0}&begin={1}&period=week&type=before&count=-300&indicator=kline".format(code, timestamp)
                                print(week_url)
                                week_df = get_data_df(week_url, 1)
                                week_df = calc_zb(week_df)
                                toweek_data = week_df.iloc[-1].to_dict()
                                print(toweek_data)
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
                                    max_ma = max(ma_data_list) if ma_data_list else 0
                                    week_max_ma = max(week_ma_data_list)
                                    if week_ma_250 == week_max_ma:
                                        week_ma_data_list.remove(week_ma_250)
                                        week_max_ma = max(week_ma_data_list)
                                except Exception as e:
                                    week_max_ma = 0
                                    max_ma = max(ma_data_list) if ma_data_list else 0
                                len_list = []
                                for x in ma_data_list:
                                    if (max_ma * 0.975) <= x:
                                        len_list.append(x)
                                #if "600020" in code:
                                #print(code, dang_qian_jia, max_ma, ya_li, ya_li_1, fang_liang, today_liang, liang_max_5days, week_max_ma, ma5_distance, day_mavol5, day_mavol10, ma5, ma10, ma20,ma30,ma60, len(len_list), atan_len)
                                if dang_qian_jia > max_ma and dang_qian_jia >= week_max_ma and len(len_list) >=(len(ma_data_list) -3):
                                    print(code)
                                    #jun_xian_distance = (ma5 - ma60)/ma60 * 100
                                    #print(day_macd, week_macd)
                                    ma_data_list.sort()
                                    #print(ma_data_list, max_ma, ma_data_list[1])
                                    jun_xian_distance = (max_ma - ma_data_list[1])/ma_data_list[1] * 100
                                    #print(jun_xian_distance)
                                    if (atan_len >=3 and len(len_list) >= 5) or (jun_xian_distance < 2.8 and atan_len >=4 and len(len_list) >=4) or (atan_len >=5 and ma5 > ma10 > ma20 > ma30 > ma60 > ma250 and jun_xian_distance < 8) and 1 > day_macd > 0:
                                    #if 1 > day_macd > 0 and jun_xian_distance < 10:# and week_macd > 0:
                                        #print(to_day_j, to_day_k, to_day_d, to_week_j,to_week_k, to_week_d)

                                        if (100 > to_day_j and to_day_d < 80):# and (100 > to_week_j > to_week_k > to_week_d and to_week_d < 80):
                                            print(df_list[1])
                                            gai_nian_url = "http://stockpage.10jqka.com.cn/{0}/".format(code[2:8])
                                            gai_nian = requests.get(gai_nian_url, headers=headers_1).text.split('dd title="')[1].split('">')[0]
                                            #logging.info(str(dtime).split()[0] + "-->" + str(name) + " ($题材概念: " + gai_nian)
                                            #name_url = "http://qt.gtimg.cn/q={0}".format(code.lower())
                                            #name = requests.get(name_url).text.split("~")[1]
                                            logging.info(day.split()[0] + "-->" + df_list[1] + " ($题材概念: " + gai_nian)
