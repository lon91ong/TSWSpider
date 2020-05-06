# -*- coding: utf-8 -*-

import requests
from time import time, sleep
from random import choice
from json import loads
#from urllib.parse import quote

novelID = '1688'
novelName = '史上最强赘婿'
#cookie = {'PHPSESSID':'atutpbhgs4h1gdsb3gjpncdkn6'}

for rl in range(19,21):
    ref_str = "https://www.ting22.com/ting/{}-{}.html".format(novelID,str(rl))
    #cookie['shistory'] = quote('think:[{}]'.format(quote(novelName)))
    #cookie[novelID+'_setURL'] = ref_str
    #cookie['index_setID'] = novelID
    sign = int(round(time() * 1000))  # 时间戳
    
    headers = {
        "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
        "Accept-encoding": "gzip, deflate, br",
        "Accept-language": "zh-CN,zh;q=0.9,zh-TW;q=0.8",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Referer": ref_str,
        "Sign": sign,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }
    getstr = "https://www.ting22.com/api.php?c=Json&id="+novelID+"&page="+str(rl+1)+"&pagesize=10&callback=jQuery21403942595757035292_{}&_={}".format(sign, sign+1)
    print('GET:',getstr)
    response = requests.get(getstr, headers=headers)
    
    json_str = response.text
    json_str = json_str.encode('raw_unicode_escape').decode('raw_unicode_escape').replace(r'\/\/', '//').replace(r'\/', '/')
    #print('jsonStr:',json_str[41:-2])
    json_data = loads(json_str[json_str.index('({')+1:-2])
    #cookie[novelID+'_setNAME'] = quote(novelName)+'('+quote(json_data["playlist"][0]["trackName"].split('(')[1][:-1])+')'+quote(' 第{}章'.format(rl*10+10))
    mp4_url_list = [x["file"] for x in json_data["playlist"]]
    #print(json_data["playlist"][0]["trackName"].split('(')[1][:-1])
    name_list = [x["pid"] for x in json_data["playlist"]]
    mp4_real_url_list = [''.join(map(chr, [int(i) for i in s.split("*")])) for s in mp4_url_list]
    
    print(mp4_real_url_list)
    print(name_list)
    ''' # 下载
    for i in range(len(mp4_url_list)):
        mp4 = requests.get(mp4_real_url_list[i])
        with open('./'+novelName+'/'+str(name_list[i])+'.mp3',"wb") as f:
            f.write(mp4.content)
            f.close()
            print('{}.mp3 -- 下载完成！'.format(name_list[i]))
    '''
    sleep(choice([0.3, 0.5, 0.8, 1.1, 1.5, 1.8, 2, 2.3, 2.5]))

import os
#print(os.listdir("./"+novelName))

def get_dir_size(dir_path):
    file_list = os.listdir(dir_path)
    size = 0
    for file_name in file_list:
        size += os.path.getsize(dir_path + "/" + file_name)
    return round(size / 1024 / 1024, 2)

print('{} MB'.format(get_dir_size("./"+novelName)))
