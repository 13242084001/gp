#import baostock as bs
import pandas as pd
import talib
import requests
import random
from hyper.contrib import HTTP20Adapter
import time, datetime
import json
import logging



logging.basicConfig(level=logging.DEBUG, format="%(message)s", filename="./xuangu.log", filemode="a")

user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29",
                   "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
                   'Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)', 'Mozilla/5.0 (compatible; U; ABrowse 0.6;  Syllable) AppleWebKit/420+ (KHTML, like Gecko)', 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)', 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR   3.5.30729)', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0;   Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;   SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; Acoo Browser; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; Avant Browser)', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1;   .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Maxthon; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)', 'Mozilla/4.0 (compatible; Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729); Windows NT 5.1; Trident/4.0)', 'Mozilla/4.0 (compatible; Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727); Windows NT 5.1; Trident/4.0; Maxthon; .NET CLR 2.0.50727; .NET CLR 1.1.4322; InfoPath.2)',
                   'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB6; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)']

headers_1 = {"user-agent": random.choice(user_agent_list),}

headers = {':authority': 'stock.xueqiu.com',
           ':method': 'GET',
           #':path': '/v5/stock/chart/kline.json?symbol=SZ000002&begin=1682323026803&period=day&type=before&count=-284&indicator=kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance',
           #':scheme': 'https',
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'accept-encoding': 'gzip, deflate, br',
           'accept-language': 'zh-CN,zh;q=0.9',
           'cache-control': 'max-age=0',
           'cookie': 'device_id=04df9bee31d96920289fbec1a4e1e03a; s=cf122uuhnb; bid=1fa9bc3995022e7a50364963f5000816_l7bkxqzb; xq_is_login=1; xq_a_token=02fe272962bcd5df06518e113f120bcfb0dc874f; xqat=02fe272962bcd5df06518e113f120bcfb0dc874f; xq_r_token=5fa7a40353195e61c8ff4647356ba9b8b23c5d9f; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjY0ODQ2ODUzODUsImlzcyI6InVjIiwiZXhwIjoxNjgzNjgxMjI3LCJjdG0iOjE2ODEwODkyMjc1NjAsImNpZCI6ImQ5ZDBuNEFadXAifQ.XXc5nUB1M5KfkqM274-k6nVUBJtSgyUpH8SvA9n7RV4PPOQxIoqkxjkm8_7RgwtlXV7yr7YDN0a6wwLoh4S_gnm68Bg0teffwke-WXYDA-fEWidiFB6ke-kBEH7JPGOXhE20cxlPUr1mZ5jioLqodH925t8XrKyR8EUcMBTZFW4Kw0ocl9u2xa-T0c4wJaL7tpTZWQpPEbxBTISq5Gm3B7CKAkAonJSVv5deOchVyvxs4M5UAe2VJjwrCpuNM2L90GJ0_qo94g0wkc65aLZN7og2QY362ag_PnFPP4t1c50Mu2bpUj_YzEGnFEc9Lm8_vDtMtWnuLpAG-RIlcpXW8w; Hm_lvt_1db88642e346389874251b5a1eded6e3=1681089228; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1682236616',
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


dtime = datetime.datetime.now()
u_time = (time.mktime(dtime.timetuple()) + 12 * 3600) * 1000
timestamp = str(u_time).split(".")[0]


#就算数据帧
def get_data_df(url):
    sessions = requests.session()
    sessions.mount(url, HTTP20Adapter())
    res = sessions.get(url, headers=headers)
    #res = requests.get(url=url, headers=headers).json()
    data_list_1 = []
    data_list = res.json().get("data").get("item")
    for data in data_list:
        tre_timeArray = time.localtime((data[0] + 13*3600*1000)/1000)
        tre_otherStyleTime = time.strftime("%Y-%m-%d", tre_timeArray)
        data[0] = str(tre_otherStyleTime)
        data_list_1.append(data)
    df = pd.DataFrame(data_list_1).drop([6, 7, 8, 9, 10, 11], axis=1)
    df = df.rename(columns={0: 'day', 1: 'liang', 2: 'open', 3: 'high', 4: 'low', 5: 'close'})
    #print(df)
    df[['open', 'close', 'low', 'high']] = df[['open', 'close', 'low', 'high']].astype('float64')
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
    df['ma250'] = talib.SMA(df['close'],timeperiod=250)
    #计算macd
    df['dif'], df['dea'], df['bar'] = talib.MACD(df['close'].values, fastperiod=12, slowperiod=26, signalperiod=9)
    return df


url =  'http://98.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112402803120599104636_1675409984210&pn=1&pz=3200&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=|0|0|0|web&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1675409984211'

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
    if i.get("f12")[:2] in ["60", "00"] and "ST" not in i.get("f14") and "-" !=  i.get("f10") and "-" != i.get("f3"):
        name = i.get("f14")
        code = 'SZ' + i.get("f12") if "00" == i.get("f12")[:2] else 'SH' + i.get("f12")
        zhang_fu = i.get("f3")
        huan_shou = i.get("f8")
        cheng_jiao_liang = i.get("f6")/100000000
        dang_qian_jia = i.get("f2")
        zui_di_jia = i.get("f16")
        zui_gao_jia = i.get("f15")
        kai_pan_jia = i.get("f17")
        #pe = i.get("f9")
        shang_ying_xian = (i.get("f15") - i.get("f2"))/i.get("f2")
        #shang_ying_xian = (i.get("f15") / ((dang_qian_jia / (((zhang_fu / 100) + 1))) - 1 - (zhang_fu / 100)
        #liu_tong_zhi = i.get("f21")/100000000
        if 1 < zhang_fu < 6 and cheng_jiao_liang > 1 and dang_qian_jia > kai_pan_jia and shang_ying_xian < 0.05 and huan_shou < 10:

            #url = "http://q.stock.sohu.com/hisHq?code=cn_{0}&start={1}&end={2}".format(code[3:], start_date.replace("-", ""), end_date.replace("-", ""))

            #url = "https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={0}&scale=240&ma=10&datalen=1200".format(code)

            day_url = "https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol={0}&begin={1}&period=day&type=before&count=-300&indicator=kline".format(code, timestamp)
        
            week_url = "https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol={0}&begin={1}&period=week&type=before&count=-300&indicator=kline".format(code, timestamp)
            #print(url)


            day_df = get_data_df(day_url)
            week_df = get_data_df(week_url)
           

            day_df = calc_zb(day_df)
            #print(day_df.iloc[-1].to_dict())
            today_data = day_df.iloc[-1].to_dict()
            yesterday_data = day_df.iloc[-2].to_dict()
            low = today_data.get('low')
            ma5 = today_data.get('ma5')
            ma5_distance = (low - ma5)/ma5 * 100
            fang_liang = yesterday_data = today_data.get('liang') / yesterday_data.get('liang')
            day_macd = today_data.get("bar") * 2
            to_day_j = today_data.get("J")
            to_day_k = today_data.get("K")
            to_day_d = today_data.get("D")
            ma_data_list = []
            for k,v in today_data.items():
                if "ma" in k:
                    if v > -99999:
                        ma_data_list.append(v)

            week_df = calc_zb(week_df)
            #print(week_df.iloc[-1].to_dict())
            toweek_data = week_df.iloc[-1].to_dict()
            week_macd = toweek_data.get("bar") * 2
            to_week_j = toweek_data.get("J")
            to_week_k = toweek_data.get("K")
            to_week_d = toweek_data.get("D")
            week_ma_data_list = []
            for k,v in toweek_data.items():
                if "ma" in k:
                    #print(type(v))
                    if v > -99999:
                        week_ma_data_list.append(v)

            #print(ma_data_list, week_ma_data_list)
            max_ma = max(ma_data_list)
            week_max_ma = max(week_ma_data_list)
            
            len_list = []
            w_len_list = []
            for x in ma_data_list:
                if (max_ma * 0.97) <= x:
                    len_list.append(x)
                    #logging.info(len(len_list))
            for x in week_ma_data_list:
                if (week_max_ma * 0.95) <= x:
                    w_len_list.append(x)
            if dang_qian_jia > max_ma  and len(len_list) >= 2 and dang_qian_jia >= week_max_ma and len(w_len_list) >= 2 and fang_liang > 1.2 and ma5_distance < 2:
                if day_macd > 0 and week_macd > 0:
                  
                    if (100 > to_day_j > to_day_k > to_day_d > 42 and to_day_d < 80) and (100 > to_week_j > to_week_k > to_week_d and to_week_d < 80):
                        #print(222222)
                        gai_nian_url = "http://stockpage.10jqka.com.cn/{0}/".format(code[2:])
                        gai_nian = requests.get(gai_nian_url, headers=headers_1).text.split('dd title="')[1].split('">')[0]
                        #print(gai_nian)
                        logging.info(str(dtime).split()[0] + "-->" + str(name) + " ($题材概念: " + gai_nian)
                        #print(name)
