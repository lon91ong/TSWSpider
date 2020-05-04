# -*- coding: utf-8 -*-

import requests
from time import time
from json import loads
from pprint import pprint

#path = "104*116*116*112*58*47*47*97*117*100*105*111*46*99*111*115*46*120*109*99*100*110*46*99*111*109*47*103*114*111*117*112*55*48*47*77*48*66*47*54*66*47*69*68*47*119*75*103*79*122*108*52*72*71*116*67*105*114*117*68*95*65*70*108*89*74*66*76*108*79*117*89*52*55*48*46*109*52*97"

#def jiema(s):
#    return ''.join(map(chr, [int(i) for i in s.split("*")]))

for rl in range(77,157):
    ref_str = "https://www.ting22.com/ting/1688-"+str(rl)+"1.html"
    cookie_str = "shistory=think%3A%5B%22%25E5%258F%25B2%25E4%25B8%258A%25E6%259C%2580%25E5%25BC%25BA%25E8%25B5%2598%25E5%25A9%25BF%22%5D; PHPSESSID=atutpbhgs4h1gdsb3gjpncdkn6; 1688_setNAME=%E5%8F%B2%E4%B8%8A%E6%9C%80%E5%BC%BA%E8%B5%98%E5%A9%BF(%E9%AB%98%E6%99%BA%E5%95%86%E8%A3%85X%E6%89%93%E8%84%B8)%20%E7%AC%AC721%E7%AB%A0; 1688_setURL=" + ref_str + "; index_setID=1688"
    cookie = {i.split("=")[0]: i.split("=")[1] for i in cookie_str.split("; ")}
    
    sign = str(int(round(time() * 1000)))
    
    headers = {
        "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
        "Accept-encoding": "gzip, deflate, br",
        "Accept-language": "zh-CN,zh;q=0.9,zh-TW;q=0.8",
        "X-Requested-With": "XMLHttpRequest",
        # "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Referer": ref_str,
        "Sign": sign,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }
    
    response = requests.get(
        "https://www.ting22.com/api.php?c=Json&id=1688&page="+str(rl+1)+"&pagesize=10&callback=jQuery21403942595757035292_{}&_={}".format(
            sign, sign), headers=headers)
    
    json_str = response.text
    json_str = json_str.encode('raw_unicode_escape').decode('raw_unicode_escape').replace(r'\/\/', '//').replace(r'\/', '/')
    #print('jsonStr:',json_str[41:-2])
    #json_data = json.loads(json_str.split("(")[1].split(")")[0])
    json_data = loads(json_str[json_str.index('({')+1:-2])
    
    mp4_url_list = [x["file"] for x in json_data["playlist"]]
    name_list = [x["pid"] for x in json_data["playlist"]]
    mp4_real_url_list = [''.join(map(chr, [int(i) for i in s.split("*")])) for s in mp4_url_list]
    
    #pprint(mp4_real_url_list)
    pprint(name_list)
    
    for i in range(len(mp4_url_list)):
        mp4 = requests.get(mp4_real_url_list[i])
        with open('./史上最强赘婿/'+str(name_list[i])+'.mp3',"wb") as f:
            f.write(mp4.content)
            f.close()

import os
print(os.listdir("./史上最强赘婿"))

def get_dir_size(dir_path):
    file_list = os.listdir(dir_path)
    size = 0
    for file_name in file_list:
        size += os.path.getsize(dir_path + "/" + file_name)
    return round(size / 1024 / 1024, 2)

print(get_dir_size("./史上最强赘婿"))
