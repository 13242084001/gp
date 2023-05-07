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


bks = ['BK0001种植业与林业', 'BK0002养殖业', 'BK0003农产品加工', 'BK0004农业服务', 'BK0005煤炭开采加工', 'BK0006石油矿业开采', 'BK0007油气开采及服务', 'BK0008化学原料', 'BK0009化学制品', 'BK0010化工合成材料', 'BK0011化工新材料', 'BK0012钢铁', 'BK0013有色冶炼加工', 'BK0014金属新材料', 'BK0015建筑材料', 'BK0016建筑装饰', 'BK0017通用设备', 'BK0018专用设备', 'BK0019仪器仪表', 'BK0020电力设备', 'BK0021半导体及元件', 'BK0022光学光电子', 'BK0023其他电子', 'BK0024消费电子', 'BK0025汽车整车', 'BK0026汽车零部件', 'BK0027非汽车交运', 'BK0028汽车服务', 'BK0029通信设备', 'BK0030计算机设备', 'BK0031白色家电', 'BK0032黑色家电', 'BK0033饮料制造', 'BK0034食品加工制造', 'BK0035纺织制造', 'BK0036服装家纺', 'BK0037造纸', 'BK0038包装印刷', 'BK0039家用轻工', 'BK0040化学制药', 'BK0041中药', 'BK0042生物制品', 'BK0043医药商业', 'BK0044医疗器械', 'BK0045电力', 'BK0046燃气', 'BK0047环保工程', 'BK0048港口航运', 'BK0049公路铁路运输', 'BK0050公交', 'BK0051机场航运', 'BK0052物流', 'BK0053房地产开发', 'BK0054园区开发', 'BK0055银行', 'BK0056保险及其他', 'BK0057证券', 'BK0058零售', 'BK0059贸易', 'BK0060景点及旅游', 'BK0061酒店及餐饮', 'BK0062通信服务', 'BK0063计算机应用', 'BK0064传媒', 'BK0065综合', 'BK0066国防军工', 'BK0067非金属材料', 'BK0068工业金属', 'BK0069贵金属', 'BK0070小金属', 'BK0071自动化设备', 'BK0072电子化学品', 'BK0073小家电', 'BK0074厨卫电器', 'BK0075医疗服务', 'BK0076房地产服务', 'BK0077互联网电商', 'BK0078教育', 'BK0079其他社会服务', 'BK0080石油加工贸易', 'BK0081环保', 'BK0082美容护理', 'BK0400ST板块', 'BK0402稀缺资源', 'BK0405生物质能', 'BK0406智能电网', 'BK0407物联网', 'BK0408移动支付', 'BK0409融资融券', 'BK0410稀土永磁', 'BK0411新疆振兴', 'BK0413石墨烯', 'BK0414云计算', 'BK0416页岩气', 'BK0417苹果概念', 'BK0418智慧城市', 'BK0419美丽中国', 'BK0425煤化工', 'BK0426智能医疗', 'BK0427生物医药', 'BK0428食品安全', 'BK0429固废处理', 'BK0430污水处理', 'BK0431创投', 'BK0432文化传媒', 'BK0433脱硫脱硝', 'BK0434电子商务', 'BK0435安防', 'BK0436特高压', 'BK0437海工装备', 'BK0438高端装备', 'BK0439特钢概念', 'BK0440天然气', 'BK0441新能源汽车', 'BK0442节能照明', 'BK0443土地流转', 'BK0444大数据', 'BK0445智能穿戴', 'BK0446互联网金融', 'BK0447手机游戏', 'BK0448网络安全', 'BK0449充电桩', 'BK0450乳业', 'BK0451特斯拉', 'BK0452上海自贸区', 'BK0453智能家居', 'BK0454在线教育', 'BK0455电子发票', 'BK0456参股民营银行', 'BK0457天津自贸区', 'BK0458民营医院', 'BK0459上海国企改革', 'BK0460一带一路', 'BK0461油品改革', 'BK0462在线旅游', 'BK0463通用航空', 'BK0464冷链物流', 'BK0465蓝宝石', 'BK0466生态农业', 'BK0467禽流感', 'BK0468尾气治理', 'BK0469京津冀一体化', 'BK0471机器人概念', 'BK0472沪股通', 'BK0473粤港澳大湾区', 'BK0474养老概念', 'BK0475白酒概念', 'BK0477黄金概念', 'BK0478光伏概念', 'BK04793D打印', 'BK0480医疗器械概念', 'BK0481三胎概念', 'BK0482家用电器', 'BK0483新材料概念', 'BK0484汽车电子', 'BK0485氟化工概念', 'BK0486小金属概念', 'BK0487金融IC', 'BK0488PM2.5', 'BK04895G', 'BK0490超导', 'BK0491金改', 'BK0493高铁', 'BK0494节能环保', 'BK0495无人机', 'BK0497大飞机', 'BK0498国产软件', 'BK0500期货概念', 'BK0501核电', 'BK0502水利', 'BK0503猪肉', 'BK0504卫星导航', 'BK0505基因测序', 'BK0506足球概念', 'BK0507职业教育', 'BK0508举牌', 'BK0509电力改革', 'BK0510中韩自贸区', 'BK0511央企国企改革', 'BK0512新股与次新股', 'BK0513网络游戏', 'BK0515阿里巴巴概念', 'BK0516体育产业', 'BK0517迪士尼', 'BK0518福建自贸区', 'BK0519工业4.0', 'BK0520参股券商', 'BK0521参股保险', 'BK0522西安自贸区', 'BK0523农村电商', 'BK0524染料', 'BK0525高送转', 'BK0526草甘膦', 'BK0527风电', 'BK0528跨境电商', 'BK0529互联网彩票', 'BK0530物流电商平台', 'BK0531碳纤维', 'BK0532两桶油改革', 'BK0533钛白粉概念', 'BK0534供应链金融', 'BK0536医药电商', 'BK0537证金持股', 'BK0539集成电路概念', 'BK0540能源互联网', 'BK0541车联网', 'BK0543高校', 'BK0544PPP概念', 'BK0545地下管网', 'BK0547深股通', 'BK0548深圳国企改革', 'BK0549军工', 'BK0550杭州亚运会', 'BK0551健康中国', 'BK0552东盟自贸区', 'BK0553乡村振兴', 'BK0554农机', 'BK0556虚拟现实', 'BK0557锂电池', 'BK0558互联网+', 'BK0559人工智能', 'BK0560参股新三板', 'BK0561量子科技', 'BK0563航运概念', 'BK0564广东自贸区', 'BK0565二维码识别', 'BK0566无人驾驶', 'BK0567电子竞技', 'BK0568OLED', 'BK0569股权转让', 'BK0570债转股(AMC概念)', 'BK0571中字头股票', 'BK0572摘帽', 'BK0573军民融合', 'BK0574雄安新区', 'BK0575MSCI概念', 'BK0576消费金融', 'BK0577共享单车', 'BK0578可燃冰', 'BK0579蚂蚁金服概念', 'BK0580特色小镇', 'BK0581参股万达商业', 'BK0583网约车', 'BK0584微信小程序', 'BK0586芯片概念', 'BK0587区块链', 'BK0588租售同权', 'BK0589人脸识别', 'BK0590装配式建筑', 'BK0591超级品牌', 'BK0593白马股', 'BK0594自由贸易港', 'BK0595互联网医疗', 'BK0596智能交通', 'BK0597互联网保险', 'BK0598无人零售', 'BK0599细胞免疫治疗', 'BK0600智能物流', 'BK0601智能音箱', 'BK0602语音技术', 'BK0603无线充电', 'BK0604燃料电池', 'BK0605腾讯概念', 'BK0606啤酒概念', 'BK0607石墨电极', 'BK0608水泥概念', 'BK0609工业互联网', 'BK0610新零售', 'BK0611小米概念', 'BK0612富士康概念', 'BK0613独角兽概念', 'BK0614网络直播', 'BK0615宁德时代概念', 'BK0616边缘计算', 'BK0617知识产权保护', 'BK0618赛马概念', 'BK0619数字中国', 'BK0620空铁WIFI', 'BK0621国产航母', 'BK0622送转填权', 'BK0623百度概念', 'BK0624燃料乙醇', 'BK0625北汽新能源', 'BK0626消费电子概念', 'BK0627国资驰援', 'BK0628壳资源', 'BK0629高送转预期', 'BK0631芬太尼', 'BK0632华为概念', 'BK0633年报预增', 'BK0634养鸡', 'BK0635柔性屏', 'BK0636大豆', 'BK0637玉米', 'BK0638农业种植', 'BK0639商誉减值', 'BK0640信托概念', 'BK0641MSCI预期', 'BK0642超清视频', 'BK0644工业大麻', 'BK0645数字孪生', 'BK0646电力物联网', 'BK0647网络切片', 'BK0648太空互联网', 'BK0649氢能源', 'BK0651冰雪产业', 'BK0652外资券商影子股', 'BK0653横琴新区', 'BK0654融媒体', 'BK0655丙烯酸', 'BK0656透明工厂', 'BK0657超级真菌', 'BK0658长三角一体化', 'BK0659黑洞概念', 'BK0661参股银行', 'BK0662台湾概念股', 'BK0663郭台铭概念', 'BK0664眼科医疗', 'BK0665人造肉', 'BK0666人民币贬值受益', 'BK0667草地贪夜蛾防治', 'BK0668数字乡村', 'BK0669华为海思概念股', 'BK0670国产操作系统', 'BK0671生物疫苗', 'BK0672动物疫苗', 'BK0673富时罗素概念股', 'BK0674黑龙江自贸区', 'BK0675烟草', 'BK0676青蒿素', 'BK0677沪伦通概念', 'BK0678垃圾分类', 'BK0679创业板重组松绑', 'BK0680仿制药一致性评价', 'BK0681半年报预增', 'BK0684中船系', 'BK0685ETC', 'BK0686氢氟酸', 'BK0687磷化工', 'BK0688光刻胶', 'BK0689钴', 'BK0690数字货币', 'BK0691标普道琼斯A股', 'BK0692无线耳机', 'BK0693一季报预增', 'BK0694非科创次新股', 'BK0695胎压监测', 'BK0696云游戏', 'BK0697澳交所概念', 'BK0698分拆上市意愿', 'BK0699MiniLED', 'BK0700网红经济', 'BK0701转基因', 'BK0702HJT电池', 'BK0703流感', 'BK0704口罩', 'BK0705云办公', 'BK0706消毒剂', 'BK0707医疗废物处理', 'BK0708航空发动机', 'BK0709氮化镓', 'BK0710超级电容', 'BK0711数据中心', 'BK0712C2M概念', 'BK0713富媒体', 'BK0714抖音概念', 'BK0715新三板精选层概念', 'BK0716REITs', 'BK0717国家大基金持股', 'BK0718海南自贸区', 'BK0719室外经济', 'BK0720中芯国际概念', 'BK0721免税店', 'BK0722新型烟草', 'BK0723NMN概念', 'BK0724可降解塑料', 'BK0725汽车拆解概念', 'BK0726环氧丙烷', 'BK0727代糖概念', 'BK0728注册制次新股', 'BK0729核准制次新股', 'BK0730科创次新股', 'BK0731第三代半导体', 'BK0732辅助生殖', 'BK0733拼多多概念', 'BK0734社区团购', 'BK0735有机硅概念', 'BK0736医美概念', 'BK0738煤炭概念', 'BK0739物业管理', 'BK0740同花顺漂亮100', 'BK0741新冠检测', 'BK0742快手概念', 'BK0743碳中和', 'BK0744光伏建筑一体化', 'BK0745高送转', 'BK0746华为汽车', 'BK0747储能', 'BK0748盐湖提锂', 'BK0749鸿蒙概念', 'BK0750共同富裕示范区', 'BK0751MCU芯片', 'BK0752牙科医疗', 'BK0753CRO概念', 'BK0754钠离子电池', 'BK0755专精特新', 'BK0756工业母机', 'BK0757PVDF概念', 'BK0758北交所概念', 'BK0759NFT概念', 'BK0760元宇宙', 'BK0761抽水蓄能', 'BK0762绿色电力', 'BK0763培育钻石', 'BK0764换电概念', 'BK0765海峡两岸', 'BK0766WiFi 6', 'BK0767智能制造', 'BK0768数据安全', 'BK0769EDR概念', 'BK0770动力电池回收', 'BK0771汽车芯片', 'BK0772传感器', 'BK0773DRG/DIP', 'BK0774柔性直流输电', 'BK0775冬奥会', 'BK0776虚拟数字人', 'BK0777预制菜', 'BK0778幽门螺杆菌概念', 'BK0779电子纸', 'BK0780新冠治疗', 'BK0781重组蛋白', 'BK0782智慧政务', 'BK0783东数西算（算力）', 'BK0784硅能源', 'BK0785PCB概念', 'BK0786民爆概念', 'BK0787净水概念', 'BK0788土壤修复', 'BK0789智慧灯杆', 'BK0790俄乌冲突概念', 'BK0791中俄贸易概念', 'BK0792跨境支付（CIPS）', 'BK0793化肥', 'BK0794托育服务', 'BK0795金属镍', 'BK0796金属锌', 'BK0797金属铅', 'BK0798金属回收', 'BK0799金属铜', 'BK0800两轮车', 'BK0801电子身份证', 'BK0802数字经济', 'BK0803国资云', 'BK0804建筑节能', 'BK0805低辐射玻璃（Low-E）', 'BK0806华为鲲鹏', 'BK0807家庭医生', 'BK0808华为欧拉', 'BK0809疫情监测', 'BK0810恒大概念', 'BK0811毛发医疗', 'BK0812碳交易', 'BK0813MicroLED概念', 'BK0814高送转', 'BK0815REITs概念', 'BK0816统一大市场', 'BK0817肝炎概念', 'BK0818露营经济', 'BK0819新型城镇化', 'BK0820噪声防治', 'BK0821方舱医院', 'BK0822猴痘概念', 'BK0823粮食概念', 'BK0824超超临界发电', 'BK0825比亚迪概念', 'BK0826F5G概念', 'BK0827汽车热管理', 'BK0900安徽', 'BK0901北京', 'BK0902重庆', 'BK0903黑龙江', 'BK0904福建', 'BK0905甘肃', 'BK0906深圳', 'BK0907广东(除深圳)', 'BK0908广西', 'BK0909贵州', 'BK0910海南', 'BK0911河北', 'BK0912河南', 'BK0913湖北', 'BK0914湖南', 'BK0915吉林', 'BK0916江苏', 'BK0917江西', 'BK0918辽宁', 'BK0919内蒙古', 'BK0920宁夏', 'BK0921青海', 'BK0922山东', 'BK0923山西', 'BK0924陕西', 'BK0925浦东', 'BK0926上海(除浦东)', 'BK0927四川', 'BK0928天津', 'BK0929西藏', 'BK0930新疆', 'BK0931云南', 'BK0932浙江']





logging.basicConfig(level=logging.INFO, format="%(message)s", filename="./xuanbankuai.log", filemode="a")

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
"""
day = "2023-04-28"

day += " 20:00:00"
time_array = time.strptime(day, format_string)
timestamp = str(int(time.mktime(time_array)) * 1000)
#u_time = (time.mktime(dtime.timetuple()) + 12 * 3600) * 1000
print(timestamp)
"""
url = "http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=sz000002&scale=5&ma=5&datalen=1023"
day_list = []
res = requests.get(url=url)
for li in res.json():
    day = li.get("day")[:10]
    if day not in day_list:
        day_list.append(day)
#bks = ['BK0049银行']
print(day_list)
for day in day_list[-2:]:
    day += " 1:00:00"
    time_array = time.strptime(day, format_string)
    timestamp = str(int(time.mktime(time_array)) * 1000)
    #u_time = (time.mktime(dtime.timetuple()) + 12 * 3600) * 1000
    print(day)
    
    bk_list = []
    if 1:
        for bk in bks:
            day_url = "https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol={0}&begin={1}&period=day&type=before&count=-300&indicator=kline".format(bk[:6], timestamp)
            #print(day_url)
            day_df = get_data_df(day_url)
            #print(day_df)
            if day_df is not None:
                today_data = day_df.iloc[-1].to_dict()
                zhang_fu = today_data.get('zhang_fu')
                huan_shou = today_data.get('huan_shou')
                last_day = today_data.get("day")
                now_day = day.split()[0]
                #cheng_jiao_e = today_data.get('cheng_jiao_e')/10000000
                high = today_data.get('high')
                dang_qian_jia = today_data.get('close')
                kai_pan_jia = today_data.get('open')
                shang_ying_xian = (high - dang_qian_jia)/dang_qian_jia
                print(zhang_fu, bk)
                if last_day == now_day:
                    if 1 < zhang_fu < 6 and dang_qian_jia > kai_pan_jia and shang_ying_xian < 0.03:
                        week_url = "https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol={0}&begin={1}&period=week&type=before&count=-300&indicator=kline".format(bk[:6], timestamp)
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
                        #print(atan5, atan10, atan20, atan30, atan60)
                        atan_len = 0
                        for atan in [atan5, atan10, atan20, atan30, atan60]:
                            if atan > 5:
                                atan_len += 1
                        yesterday_liang = yesterday_data.get('liang')
                        fang_liang = today_liang / yesterday_liang
                        day_mavol5 = today_data.get('vol5')
                        day_mavol10 = today_data.get('vol10')
                        day_macd = today_data.get('bar') * 2
                        to_day_k = today_data.get("K")
                        to_day_j = today_data.get("J")
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
                        len_list = []
                        for x in ma_data_list:
                            if (max_ma * 0.97) <= x:
                                len_list.append(x)
                        print(ya_li, dang_qian_jia, max_ma, week_max_ma, ya_li_1, fang_liang, today_liang, liang_max_5days, len(len_list), ma5_distance, day_mavol5, day_mavol10, ma5, ma10, ma20, ma30, ma60, ma250, atan_len)
                        if dang_qian_jia > max_ma and ya_li > 0.5 and ya_li_1 < 0.5 and fang_liang > 1.2 and today_liang > liang_max_5days and dang_qian_jia >= week_max_ma and ma5_distance < 1 and day_mavol5 > day_mavol10 and ma5 > ma10 and len(len_list) >=3 and atan_len >=3:
                            ma_data_list.sort()
                            jun_xian_distance = (max_ma - ma_data_list[2])/ma_data_list[2] * 100
                            #print(jun_xian_distance)
                            if (jun_xian_distance < 2 and len(len_list) >=4) or (2 < jun_xian_distance < 5 and atan_len >=4 and len(len_list) >=4) or (jun_xian_distance > 5 and atan_len >=5):
                                #print(2222222222, bk, jun_xian_distance, atan5, atan10, atan20, atan30, atan60)
                                #print(day_macd, week_macd)
                                if day_macd > 0 and 0 < jun_xian_distance < 5:# and week_macd > 0:
                                    #print(to_day_j, to_day_k, to_day_d, to_week_j,to_week_k, to_week_d)

                                    if (to_day_j > to_day_k > to_day_d and to_day_d < 80):# and (100 > to_week_j > to_week_k > to_week_d and to_week_d < 80):
                                    #print(3333333333)
                                        bk_list.append(bk)
        print(bk_list)
        
        #bk_list = ["BK0799"]
        all_code = []
        for bk in bk_list:
            bk_co_url = "https://stock.xueqiu.com/v5/stock/forum/stocks.json?ind_code={0}".format(bk[:6])
            #print(bk_co_url)
            #time.sleep(0.5)
            sessions = requests.session()
            sessions.mount(bk_co_url, HTTP20Adapter())
            res = sessions.get(bk_co_url, headers=headers)
            #print(res.text)
            bk_code_list = res.json().get("data").get("items")
            for co in bk_code_list:
                #print(1111, co)
                if co.get("symbol")[2:4] in ["00", "60"]:
                    #print(222, co)
                    all_code.append(co.get("symbol"))
         

        code_list_last = []
        for i in range(0, len(all_code), 100):
            tmp_list = all_code[i:i+100]
            code_name_list_url = "https://stock.xueqiu.com/v5/stock/batch/quote.json?symbol={0}".format(",".join(tmp_list))
            #print(code_name_list_url)
            res = requests.get(code_name_list_url, headers=headers_1)
            all_code_list = res.json().get("data").get("items")
            for code in all_code_list:
                name = code.get("quote").get("name")
                symbol = code.get("quote").get("symbol")
                code_list_last.append(symbol+name)
        code_list_last = set(code_list_last)
        print(code_list_last, len(code_list_last))
        code_list_query = [i[2:8] for i in code_list_last]


        #url =  'http://98.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112402803120599104636_1675409984210&pn=1&pz=3200&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=|0|0|0|web&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1675409984211'
        #res = requests.get(url=url)
        #yyx_str = res.text.split('data":')[1].split("})")[0]
        #print(yyx_str)
        #yyx_json = json.loads(yyx_str)
        #print(yyx_json)
        #data = yyx_json.get("diff")

        for code in  code_list_last:
            #print(i.get("f12")[:2])
            #if "00" == i.get("f12")[:2] and "ST" not in i.get("f14"):
            if code[2:4] in ["60", "00"] and "ST" not in code:# and i.get("f12") in code_list_query:
                #print(i.get("f14"))
                """
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
                """
                day_url = "https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol={0}&begin={1}&period=day&type=before&count=-300&indicator=kline".format(code[:8], timestamp)
                print(day_url)
                day_df = get_data_df(day_url)
                if day_df is not None:
                    #code = 'SZ' + code if "00" == code[:2] else 'SH' + code
                    #print(day_df)
                    today_data = day_df.iloc[-1].to_dict()
                    cheng_jiao_e = today_data.get('cheng_jiao_e')/10000000
                    high = today_data.get('high')
                    dang_qian_jia = today_data.get('close')
                    kai_pan_jia = today_data.get('open')
                    shang_ying_xian = (high - dang_qian_jia)/dang_qian_jia
                    zhang_fu = today_data.get('zhang_fu')
                    huan_shou = today_data.get('huan_shou')
                if 1.5 < zhang_fu < 6 and cheng_jiao_e > 0.6 and dang_qian_jia > kai_pan_jia and shang_ying_xian < 0.05 and huan_shou < 10:
                    """
                    day_url = "https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol={0}&begin={1}&period=day&type=before&count=-300&indicator=kline".format(code, timestamp)
                    #print(day_url)
                    day_df = get_data_df(day_url)
                    """
                    print(1111111)
                    if day_df is not None:
                        #print(11111)
                        week_url = "https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol={0}&begin={1}&period=week&type=before&count=-300&indicator=kline".format(code[:8], timestamp)
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
                            if atan > 5:
                                atan_len += 1
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
                        len_list = []
                        for x in ma_data_list:
                            if (max_ma * 0.975) <= x:
                                len_list.append(x)
                        #if "600020" in code:
                        #print(code, dang_qian_jia, max_ma, ya_li, ya_li_1, fang_liang, today_liang, liang_max_5days, week_max_ma, ma5_distance, day_mavol5, day_mavol10, ma5, ma10, ma20,ma30,ma60, len(len_list), atan_len)
                        if dang_qian_jia > max_ma and ya_li > 0.5 and ya_li_1 < 0.5 and fang_liang > 1.2 and today_liang > liang_max_5days and dang_qian_jia >= week_max_ma and ma5_distance < 1 and day_mavol5 > day_mavol10 and round(ma5, 7) >= round(ma10, 7) and len(len_list) >=4 and atan_len >=3:
                            print(code[8:])
                            #jun_xian_distance = (ma5 - ma60)/ma60 * 100
                            #print(day_macd, week_macd)
                            ma_data_list.sort()
                            jun_xian_distance = (max_ma - ma_data_list[2])/ma_data_list[2] * 100
                            #print(jun_xian_distance)
                            if (jun_xian_distance < 2 and len(len_list) >=4) or (2 < jun_xian_distance < 5 and atan_len >=4 and len(len_list) >=4) or (jun_xian_distance > 5 and atan_len >=5) and 1 > day_macd > 0:
                            #if 1 > day_macd > 0 and jun_xian_distance < 10:# and week_macd > 0:
                                #print(to_day_j, to_day_k, to_day_d, to_week_j,to_week_k, to_week_d)
                      
                                if (100 > to_day_j and to_day_d < 80):# and (100 > to_week_j > to_week_k > to_week_d and to_week_d < 80):
                                    #print(3333333333)
                                    gai_nian_url = "http://stockpage.10jqka.com.cn/{0}/".format(code[2:8])
                                    gai_nian = requests.get(gai_nian_url, headers=headers_1).text.split('dd title="')[1].split('">')[0]
                                    #logging.info(str(dtime).split()[0] + "-->" + str(name) + " ($题材概念: " + gai_nian)
                                    logging.info(day.split()[0] + "-->" + str(code[8:]) + " ($题材概念: " + gai_nian)
