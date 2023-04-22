# coding=utf-8
import requests
import random
import io
import logging
import json
import datetime, time, sys
from statistics import mean
# 选择站上所有均线的票，日k，周k
#sys.stdout = io.TextIOWrapper(io.BufferedWriter(sys.stdout.buffer, 5), encoding='utf-8')

logging.basicConfig(level=logging.DEBUG, format="%(message)s", filename="./all_junxian.log", filemode="a")



"""
code_all_url = "https://stockapi.com.cn/v1/base/all?token=a20428f5bc97e60c6918a15e032079b41a3872df60575e1d"
code_all_list = requests.get(url=code_all_url).json().get("data")
print(len(code_all_list))
code_list = []
for code in code_all_list:
    if code.get("api_code")[:2] in ["60", "00"] and ("ST" not in code.get("name")):
        code_list.append(code.get("api_code"))
print(code_list)
print(len(code_list))
"""

url =  'http://98.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112402803120599104636_1675409984210&pn=1&pz=8000&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=|0|0|0|web&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1675409984211'

res = requests.get(url=url)
yyx_str = res.text.split('data":')[1].split("})")[0]
#print(yyx_str)
yyx_json = json.loads(yyx_str)
#print(yyx_json)
data = yyx_json.get("diff")
code_list = []
for i in data:
    try:
        if i.get("f12")[:2] in ["60", "00"] and "ST" not in i.get("f14") and "退" not in i.get("f14") and "-" !=  i.get("f10") and "-" != i.get("f3") and i.get("f3") > 0:
            code_list.append(i.get("f12"))
    except Exception as e:
        print(e)
        print(i.get("f14"))
print(code_list, len(code_list))



#code_list = ['000403']


user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29",
                   "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
                   'Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)', 'Mozilla/5.0 (compatible; U; ABrowse 0.6;  Syllable) AppleWebKit/420+ (KHTML, like Gecko)', 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)', 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR   3.5.30729)', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0;   Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;   SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; Acoo Browser; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; Avant Browser)', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1;   .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Maxthon; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)', 'Mozilla/4.0 (compatible; Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729); Windows NT 5.1; Trident/4.0)', 'Mozilla/4.0 (compatible; Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727); Windows NT 5.1; Trident/4.0; Maxthon; .NET CLR 2.0.50727; .NET CLR 1.1.4322; InfoPath.2)',
                   'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB6; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)']

headers = {"user-agent": random.choice(user_agent_list),}


url = "http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=sz000002&scale=5&ma=5&datalen=1023"
day_list = []
res = requests.get(url=url)
for li in res.json():
    day = li.get("day")[:10]
    if day not in day_list:
        day_list.append(day)

day_list = day_list[1:]
print(day_list)
for day in day_list[-1:]:
    des_code_list = []
    for code in code_list:
        #logging.info(day_list[-2])
        day_data_url = "http://q.stock.sohu.com/hisHq?code=cn_{0}&start={1}&end={2}".format(code, day.replace("-", ""), day.replace("-", ""))
        z_day_data_url = "http://q.stock.sohu.com/hisHq?code=cn_{0}&start={1}&end={2}".format(code, day_list[-2].replace("-", ""), day_list[-2].replace("-", ""))     
        sz_day_data_url = "http://q.stock.sohu.com/hisHq?code=cn_{0}&start={1}&end={2}".format(code, "2023-04-21".replace("-", ""), "2023-04-21".replace("-", ""))
        try: 
            #print(day_data_url)
            tmp_response_1 = requests.get(url=day_data_url, headers=headers).json()
            #logging.info(tmp_response_1)
            z_tmp_response_1 = requests.get(url=z_day_data_url, headers=headers).json()
            sz_tmp_response_1 = requests.get(url=sz_day_data_url, headers=headers).json()
            #logging.info(z_tmp_response_1)
            tmp_response = tmp_response_1[0].get("hq")[0]
            z_tmp_response = z_tmp_response_1[0].get("hq")[0]
            sz_tmp_response = sz_tmp_response_1[0].get("hq")[0]
        except Exception as e:
            #print(111111)
            #if 2 == tmp_response_1[0].get("status"):
            logging.info("111111", e, code)
                
            continue
        
        #logging.info("7777777777777777")
        zhang_fu = float(tmp_response[4][:-1])
        huan_shou = float(tmp_response[-1][:-1])
        #shou_shu = float(tmp_response[-3])
        cheng_jiao_liang = float(tmp_response[-2])/ 10000
        shou_pan_jia = float(tmp_response[2])
        z_shou_pan_jia = float(z_tmp_response[2])
        #print(z_shou_pan_jia)
        sz_shou_pan_jia = float(sz_tmp_response[2])
        zui_di_jia = float(tmp_response[5])
        kai_pan_jia = float(tmp_response[1])
        #shang_ying_xian = (float(tmp_response[-4]) - float(tmp_response[2])) / float(tmp_response[2])
        shang_ying_xian = float(tmp_response[-4]) / (float(tmp_response[2])/(zhang_fu/100 + 1)) - 1 - zhang_fu/100
        #print(shang_ying_xian, float(tmp_response[-4]), float(tmp_response[2]), zhang_fu)
        #print(float(tmp_response[-4]), float(tmp_response[2]))
        #print("666666666666")
        #logging.info("7777777777777777")
        if (1.5< zhang_fu < 6) and cheng_jiao_liang > 1 and shou_pan_jia > kai_pan_jia and shang_ying_xian < 0.05:
            #print("4444444444")
            ma_url="https://stockapi.com.cn/v1/quota/ma?token=a20428f5bc97e60c6918a15e032079b41a3872df60575e1d&code={0}&date={1}&ma=5,10,20,30,60,250&rehabilitation=100&calculationCycle=100".format(code, day)
            week_ma_url="https://stockapi.com.cn/v1/quota/ma?token=a20428f5bc97e60c6918a15e032079b41a3872df60575e1d&code={0}&date={1}&ma=5,10,20,30,60,250&rehabilitation=100&calculationCycle=101".format(code, day)
            z_ma_url="https://stockapi.com.cn/v1/quota/ma?token=a20428f5bc97e60c6918a15e032079b41a3872df60575e1d&code={0}&date={1}&ma=5,10,20,30,60,250&rehabilitation=100&calculationCycle=100".format(code, day_list[-2])
            z_week_ma_url="https://stockapi.com.cn/v1/quota/ma?token=a20428f5bc97e60c6918a15e032079b41a3872df60575e1d&code={0}&date={1}&ma=5,10,20,30,60,250&rehabilitation=100&calculationCycle=101".format(code, day_list[-2])
            #print(ma_url)
            res_1 = requests.get(url=ma_url)
            res_2 = requests.get(url=week_ma_url)
            z_res_1 = requests.get(url=z_ma_url)
            z_res_2 = requests.get(url=z_week_ma_url)
            #print(res_1.json())
            try:
                ma_data = res_1.json().get("data")
                ma_data_list = []
                if ma_data.get("ma5"):
                    ma_data_list.append(ma_data.get("ma5"))
                if ma_data.get("ma10"):
                    ma_data_list.append(ma_data.get("ma10"))
                if ma_data.get("ma20"):
                    ma_data_list.append(ma_data.get("ma20"))
                if ma_data.get("ma30"):
                    ma_data_list.append(ma_data.get("ma30"))
                if ma_data.get("ma60"):
                    ma_data_list.append(ma_data.get("ma60"))
                if ma_data.get("ma250"):
                    ma_data_list.append(ma_data.get("ma250"))
           
                week_ma_data = res_2.json().get("data")
                week_ma_data_list = []
                if week_ma_data.get("ma5"):
                    week_ma_data_list.append(week_ma_data.get("ma5"))
                if week_ma_data.get("ma10"):
                    week_ma_data_list.append(week_ma_data.get("ma10"))
                if week_ma_data.get("ma20"):
                    week_ma_data_list.append(week_ma_data.get("ma20"))
                if week_ma_data.get("ma30"):
                    week_ma_data_list.append(week_ma_data.get("ma30"))
                if week_ma_data.get("ma60"):
                    week_ma_data_list.append(week_ma_data.get("ma60"))
                if week_ma_data.get("ma250"):
                    week_ma_data_list.append(week_ma_data.get("ma250"))
                ma_data_list = [float(x) for x in ma_data_list]
                max_ma = max(ma_data_list)
                week_ma_data_list = [float(x) for x in week_ma_data_list]
                week_max_ma = max(week_ma_data_list)


                z_ma_data = z_res_1.json().get("data")
                z_ma_data_list = []
                if z_ma_data.get("ma5"):
                    z_ma_data_list.append(z_ma_data.get("ma5"))
                if z_ma_data.get("ma10"):
                    z_ma_data_list.append(z_ma_data.get("ma10"))
                if z_ma_data.get("ma20"):
                    z_ma_data_list.append(z_ma_data.get("ma20"))
                if z_ma_data.get("ma30"):
                    z_ma_data_list.append(z_ma_data.get("ma30"))
                if z_ma_data.get("ma60"):
                    z_ma_data_list.append(z_ma_data.get("ma60"))
                if z_ma_data.get("ma250"):
                    z_ma_data_list.append(z_ma_data.get("ma250"))
           
                z_week_ma_data = z_res_2.json().get("data")
                z_week_ma_data_list = []
                if z_week_ma_data.get("ma5"):
                    z_week_ma_data_list.append(z_week_ma_data.get("ma5"))
                if week_ma_data.get("ma10"):
                    z_week_ma_data_list.append(z_week_ma_data.get("ma10"))
                if z_week_ma_data.get("ma20"):
                    z_week_ma_data_list.append(z_week_ma_data.get("ma20"))
                if z_week_ma_data.get("ma30"):
                    z_week_ma_data_list.append(z_week_ma_data.get("ma30"))
                if z_week_ma_data.get("ma60"):
                    z_week_ma_data_list.append(z_week_ma_data.get("ma60"))
                if z_week_ma_data.get("ma250"):
                    z_week_ma_data_list.append(z_week_ma_data.get("ma250"))
                z_ma_data_list = [float(x) for x in z_ma_data_list]
                z_max_ma = max(z_ma_data_list)
                z_week_ma_data_list = [float(x) for x in z_week_ma_data_list]
                z_week_max_ma = max(z_week_ma_data_list)

                #logging.info(str(shou_pan_jia) + "---" + str(max_ma) + "--" + str(week_max_ma) + "--" + str(sz_shou_pan_jia) + "--" + str(z_week_max_ma) + "--" + str(len(z_week_ma_data_list)) + "--" + str(z_max_ma))
                m = n = 0
                if shou_pan_jia >= week_max_ma and sz_shou_pan_jia < z_week_max_ma and 6 == len(z_week_ma_data_list):
                    #logging.info("1111111")
                    #print(type(z_week_max_ma))
                    #print(type(z_week_ma_data.get("ma250")))
                    if z_week_max_ma == float(z_week_ma_data.get("ma250")):
                        m = 1
                        #logging.info("222222222")
                #print(z_shou_pan_jia, z_max_ma, len(z_ma_data_list))
                if z_shou_pan_jia < z_max_ma and 6 == len(z_ma_data_list):
                    #logging.info("33333333333")
                    if z_max_ma == float(z_ma_data.get("ma250")):
                        #logging.info("4444444444")
                        n = 1
                if shou_pan_jia > max_ma and (m or n):
                    code_1 = "sz" + code if "00" == code[:2] else "sh" + code
                    name_url = "http://qt.gtimg.cn/q={0}".format(code_1)
                    name = requests.get(name_url).text.split("~")[1]
                    gai_nian_url = "http://stockpage.10jqka.com.cn/{0}/".format(code)
                    gai_nian = requests.get(gai_nian_url, headers=headers).text.split('dd title="')[1].split('">')[0]
                    logging.info(str(day) + str(name) + " (" + gai_nian)
                    #print(i.get("f12"))
            
            except Exception as e:
                print(e)
                #if 2 == tmp_response_1[0].get("status"):
                logging.info("222222", e)
                
                continue
    
