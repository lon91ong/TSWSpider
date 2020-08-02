# -*- coding: utf-8 -*-

import requests
from time import time, sleep
from random import choice
from json import loads
from re import search as se
from os import path, makedirs, listdir
#from urllib.parse import quote

novelID = '1740'
novelName = '大王饶命'
#cookie = {'PHPSESSID':'atutpbhgs4h1gdsb3gjpncdkn6'}
if not path.exists(novelName): makedirs(novelName)

for rl in range(0,116):
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
        "Sign": str(sign),
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }
    getstr = "https://www.ting22.com/api.php?c=Json&id="+novelID+"&page="+str(rl+1)+"&pagesize=10&callback=jQuery21403942595757035292_{}&_={}".format(sign, sign+1)
    #print('GET:',getstr)
    sucFlag = False
    while not sucFlag:
        response = requests.get(getstr, headers=headers)
    
        json_str = response.text.replace(r'\/', '/')
        #json_str = json_str.encode('raw_unicode_escape').decode('raw_unicode_escape').replace(r'\/\/', '//').replace(r'\/', '/')
        try:
            json_data = loads(json_str[json_str.index('({')+1:-2])
            sucFlag = True
        except ValueError:
            print('retry rl:{}'.format(rl))
            sleep(30)

    #cookie[novelID+'_setNAME'] = quote(novelName)+'('+quote(json_data["playlist"][0]["trackName"].split('(')[1][:-1])+')'+quote(' 第{}章'.format(rl*10+10))
    mp4_url_list = [''.join(map(chr, [int(i) for i in x["file"].split("*")])) for x in json_data["playlist"]]
    #print(json_data["playlist"][0]["trackName"].split('(')[1][:-1])
    name_list = [x["pid"] for x in json_data["playlist"]]
    
    #print('文件地址:\n', mp4_url_list)
    #print('章节:', name_list)
    # 下载
    for i in range(len(mp4_url_list)):
        try: # 跳过已下载的文件
            size = round(path.getsize('./'+novelName+'/'+str(name_list[i])+'.mp3') / 1024 / 1024, 2)
        except FileNotFoundError:
            size = 0
            pass
        if size < 2: # 小于2MB的重下一遍
            sleep(choice([0.3, 0.5, 0.8, 1.1]))
            sucFlag = False
            while not sucFlag:
                try:
                    if se(r'(?<=/)\d+(?=\$xm)', mp4_url_list[i]) is not None: # 免费试听节目
                        mp4 = requests.get('http://mobile.ximalaya.com/mobile/redirect/free/play/{}/0'.format(se(r'(?<=/)\d+(?=\$xm)', mp4_url_list[i]).group()),verify=False, timeout=10)
                    else: # 收费节目
                        mp4 = requests.get(mp4_url_list[i],verify=False, timeout=10)
                    with open('./'+novelName+'/'+str(name_list[i])+'.mp3',"wb") as f:
                        f.write(mp4.content)
                        f.close()
                        sucFlag = True
                        print('{}.mp3 -- 下载完成！-- {}MB'.format(name_list[i],round(len(mp4.content) / 1024 / 1024, 2)))
                except:
                    print('retry rl:{},file No.{}'.format(rl,name_list[i]))
                    sleep(30)
        else:
            size =i
    if size != len(name_list)-1:
        #print('skip:'+str(rl*10+10))
    #else:
        sleep(choice([2.2, 3.2, 4, 4.3, 4.9]))


#print(os.listdir("./"+novelName))

def get_dir_size(dir_path):
    file_list = listdir(dir_path)
    size = 0
    for file_name in file_list:
        size += path.getsize(dir_path + "/" + file_name)
    return round(size / 1024 / 1024, 2)

print('{} MB'.format(get_dir_size("./"+novelName)))
