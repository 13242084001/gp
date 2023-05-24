import requests, json
"""
url =  'http://98.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112402803120599104636_1675409984210&pn=1&pz=6000&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=|0|0|0|web&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1675409984211'

res = requests.get(url=url)
yyx_str = res.text.split('data":')[1].split("})")[0]
#print(yyx_str)
yyx_json = json.loads(yyx_str)
#print(yyx_json)
data = yyx_json.get("diff")
code_dict = {}
for i in  data:
            #print(i.get("f12")[:2])
    if i.get("f12")[:2] in ["60", "00"] and "ST" not in i.get("f14") and "-" != i.get("f6"):
        code_dict[i.get("f12")] = i.get("f14")

print(code_dict)
"""
import code_dict
i = 0
for k,v in code_dict.code_dict.items():
    i += 1
    if "002557" == k:
        print(i)
