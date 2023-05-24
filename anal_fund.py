# coding=utf-8
#输入基金代码，打印个季度持仓及基本信息
from bs4 import BeautifulSoup
import sys
import requests
import random
from prettytable import from_html
import io
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
from urllib3.util import Retry
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

all_jd_list = []

format_string="%Y-%m-%d %H:%M:%S"

user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29",
                   "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
                   'Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)', 'Mozilla/5.0 (compatible; U; ABrowse 0.6;  Syllable) AppleWebKit/420+ (KHTML, like Gecko)', 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)', 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR   3.5.30729)', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0;   Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;   SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; Acoo Browser; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; Avant Browser)', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1;   .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Maxthon; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)', 'Mozilla/4.0 (compatible; Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729); Windows NT 5.1; Trident/4.0)', 'Mozilla/4.0 (compatible; Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727); Windows NT 5.1; Trident/4.0; Maxthon; .NET CLR 2.0.50727; .NET CLR 1.1.4322; InfoPath.2)',
                   'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB6; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)']


def anla_chi_cang_html(fund, year):
    zcgm_url = "http://fundf10.eastmoney.com/ccmx_{0}.html".format(fund,)
    headers_0 = { "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                  "Accept-Encoding": "gzip, deflate",
                  "Accept-Language": "zh-CN,zh;q=0.9",
                  #"Cache-Control": "max-age=0",
                  "Connection": "keep-alive",
                  #"Cookie": "EMFUND1=null; EMFUND3=null; EMFUND2=null; EMFUND4=null; EMFUND5=null; qgqp_b_id=7143716b34a58fe86b3f407c67112b77; st_si=67265165850040; st_asi=delete; ASP.NET_SessionId=kjs5xcotsllp3aekv0qsedi0; EMFUND0=null; EMFUND6=03-07%2016%3A39%3A44@%23%24%u6613%u65B9%u8FBE%u6807%u666E%u6D88%u8D39%u54C1%u6307%u6570A@%23%24118002; EMFUND7=04-01%2017%3A29%3A29@%23%24%u534E%u590F%u80FD%u6E90%u9769%u65B0%u80A1%u7968A@%23%24003834; EMFUND9=04-08%2010%3A05%3A17@%23%24%u534E%u6CF0%u67CF%u745E%u4E9A%u6D32%u9886%u5BFC%u4F01%u4E1A%u6DF7%u5408@%23%24460010; td_cookie=4006508035; EMFUND8=04-08 14:22:38@#$%u8D22%u901A%u4EF7%u503C%u52A8%u91CF%u6DF7%u5408@%23%24720001; st_pvi=59649223508013; st_sp=2022-03-07%2016%3A39%3A44; st_inirUrl=http%3A%2F%2Ffund.eastmoney.com%2F118002.html; st_sn=101; st_psi=20220408142249287-112200305283-9155663238",
                  "Host": "fundf10.eastmoney.com",
                  #"Referer": "http://fund.eastmoney.com/",
                  "Upgrade-Insecure-Requests": "1",
                  "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
            }
    res = requests.get(zcgm_url, headers=headers_0)
    #print(res.text)
    soup = BeautifulSoup(res.text, "html.parser")
    des_div = soup.find("div", class_="bs_gl")
    for a in des_div.find_all("a"):
      
        a.replace_with("%s" % a.string)

    for span in des_div.find_all("span"):
        span.replace_with("%s" % span.string)
    for label in des_div.find_all("label"):
        print(label.text.strip())
    print(" ")
    print(" ")

    headers = {"Accept": "*/*",
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh-CN,zh;q=0.9",
               "Connection": "keep-alive",
               "Cookie": "EMFUND1=null; EMFUND2=null; EMFUND3=null; EMFUND4=null; EMFUND5=null; EMFUND6=null; qgqp_b_id=7143716b34a58fe86b3f407c67112b77; st_si=67265165850040; st_asi=delete; ASP.NET_SessionId=kjs5xcotsllp3aekv0qsedi0; EMFUND0=null; EMFUND7=03-07%2016%3A39%3A44@%23%24%u6613%u65B9%u8FBE%u6807%u666E%u6D88%u8D39%u54C1%u6307%u6570A@%23%24118002; EMFUND8=04-01%2017%3A29%3A29@%23%24%u534E%u590F%u80FD%u6E90%u9769%u65B0%u80A1%u7968A@%23%24003834; EMFUND9=04-07 15:24:57@#$%u8D22%u901A%u4EF7%u503C%u52A8%u91CF%u6DF7%u5408@%23%24720001; st_pvi=59649223508013; st_sp=2022-03-07%2016%3A39%3A44; st_inirUrl=http%3A%2F%2Ffund.eastmoney.com%2F118002.html; st_sn=29; st_psi=2022040715251816-112200305283-8374870842; td_cookie=3924229445",
               "Host": "fundf10.eastmoney.com",
               "Referer": "http://fundf10.eastmoney.com/ccmx_{0}.html".format(fund,),
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
}
    chi_cang_url = "http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code={0}&topline=10&year={1}&month=&rt={2}".format(fund, year, str(random.uniform(0, 1)))
    res = requests.get(chi_cang_url, headers=headers)
    res_str = res.text.split("\"")[1]
    #print(res_str)
    if not res_str:
        return []
    soup = BeautifulSoup(res_str, "html.parser")
    for a in soup.find_all("a"):
        a.replace_with("%s" % a.string)
   
    for span in soup.find_all("span"):
        span.replace_with("%s" % span.string)
    #print(soup)
    #four_chi_cang_10_tr = soup.find_all("tbody")[0].find_all("tr")
    four_chi_cang_table_all = soup.find_all("table")#class_="w782 comm tzxq")
    #print(four_chi_cang_table_all)
    #print(four_chi_cang_10_tr)
    for table in four_chi_cang_table_all:
        code_list = []
        tb = from_html(str(table))
        print(tb[0])
        for tr in table.find_all("tr"):
            #print(tr)
            if tr.find_all("td"):
                td = tr.find_all("td")[1].string
                print(td)
                code_list.append(td)
        #print(code_list)
        all_jd_list.append(code_list)
            
    #return code_list

fund = str(sys.argv[1])
for year in ["2023", "2022", "2021"]:
    anla_chi_cang_html(fund, year)

#print(all_jd_list)

last_add_list = []
for ind, li in enumerate(all_jd_list):
    try:
        result = list(set(li).difference(set(all_jd_list[ind+1])))
        #print(result)
        last_add_list.append(result)
    except Exception as e:
        pass

print(last_add_list)

gong_gao_url = "http://api.fund.eastmoney.com/f10/JJGG?callback=jQuery18306072087503684447_1684916632984&fundcode=004685&pageIndex=1&pageSize=20&type=3&_=1684916633005"

headers = {'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': 'qgqp_b_id=ea4adf46f1bc3db9159d15f087aef159; em-quote-version=topspeed; HAList=ty-0-002091-%u6C5F%u82CF%u56FD%u6CF0%2Ca-sz-000002-%u4E07%20%20%u79D1%uFF21%2Cty-0-000970-%u4E2D%u79D1%u4E09%u73AF%2Cty-0-300059-%u4E1C%u65B9%u8D22%u5BCC%2Cty-0-399001-%u6DF1%u8BC1%u6210%u6307%2Cty-1-688327-%u4E91%u4ECE%u79D1%u6280-UW; EMFUND1=null; EMFUND2=null; EMFUND3=null; EMFUND4=null; EMFUND5=null; EMFUND6=null; EMFUND7=null; EMFUND8=null; EMFUND0=null; EMFUND9=04-27 08:54:18@#$%u534E%u590F%u4E2D%u8BC1%u52A8%u6F2B%u6E38%u620FETF%u8054%u63A5A@%23%24012768; st_si=71024820079034; st_asi=delete; st_pvi=98948562751532; st_sp=2022-09-21%2017%3A26%3A02; st_inirUrl=https%3A%2F%2Femdatah5.eastmoney.com%2F; st_sn=9; st_psi=20230524162347289-112200305283-2217962658',
    'Host': 'api.fund.eastmoney.com',
    'Referer': 'http://fundf10.eastmoney.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}


res = requests.get(gong_gao_url, headers=headers)
st = res.text.split("(")[1].split(")")[0]
import json

sts = json.loads(st).get("Data")
#print(sts)

date_list = []
for st in sts:
   if "季度报告" in st.get("TITLE"):
       date_list.append(st.get("PUBLISHDATEDesc"))



data_dict = dict(zip(date_list[0:len(last_add_list)-1], last_add_list))

url = "http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=sz000002&scale=5&ma=5&datalen=60"
day_list = []
res = requests.get(url=url)
for li in res.json():
    day = li.get("day")[:10]
    if day not in day_list:
        day_list.append(day)
for day in day_list[-1:]:
    day += " 16:00:00"
    time_array = time.strptime(day, format_string)
    timestamp = str(int(time.mktime(time_array)) * 1000)
    #u_time = (time.mktime(dtime.timetuple()) + 12 * 3600) * 1000
    print(day)


def get_data_df(url):
    sessions = requests.session()
    sessions.mount(url, HTTP20Adapter(max_retries=Retry(total=5, status_forcelist=[500, 501, 502, 503, 504, 505, 506, 507, 508, 509])))
    res = sessions.get(url, headers=headers, timeout=20)
    #res = requests.get(url=url, headers=headers).json()
    data_list_1 = []
   # print(res.status_code)
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

for k,v in data_dict.items():
    zhang_fu = 0
    for code in v:
        code = 'SZ' + code if "00" == code[:2] else 'SH' + code
        day_url = "https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol={0}&begin={1}&period=day&type=before&count=-1000&indicator=kline".format(code, timestamp)
        day_df = get_data_df(day_url)
        dd = day_df.loc[k:].iloc[0:30]
        zhang_fu += (dd.iloc[-1].to_dict().get("close") - dd.iloc[0].to_dict().get("close"))/dd.iloc[0].to_dict().get("close") * 100
        #print(t_zf)
    print(zhang_fu/len(v))
    print("=================")
