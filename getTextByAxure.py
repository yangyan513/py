# pip install pandas
# pip install openpyxl
# pip install requests

import requests
import json
import re
from bs4 import BeautifulSoup
import unicodedata
import csv
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0'}

# Load proInfo
url = "https://example.cn/locales/render/product_basic.json"

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    proInfo = response.json()
except (requests.HTTPError, requests.ConnectionError):
    proInfo = {'products': {}}

# # From proInfo, fetch the required name and name+(Lifetime)
names = {p["name"] for p in proInfo["products"].values()}
names.update(p["name"] + " (Lifetime)" for p in proInfo["products"].values())
##去掉关键词
names.update(p["name"].replace("Streamfab", "").replace("DVDFab", "").strip() for p in proInfo["products"].values())
names.update((p["name"] + " (Lifetime)").replace("Streamfab", "").replace("DVDFab", "").strip() for p in proInfo["products"].values())


# 原型图链接
data = [{
 "html_url": "https://example.cn/%E8%B4%AD%E4%B9%B0%E5%BC%B9%E7%AA%97%E5%A2%9E%E5%8A%A0365_%E5%85%A8%E6%96%B0%E7%94%A8%E6%88%B7.html",
}]

outputInfo = {
    "file_name": "common_product.json",
    "file_url": "https://example.cn/locales/en/common_product.json",
    "compare_file":[ "https://example.cn/locales/en/common_product.json","https://example.cn/locales/en/common.json"]
}

# 异常处理和获取内容更健壮并且函数化
def get_response(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        return response.text
    except (requests.HTTPError, requests.ConnectionError):
        return ""


def get_filtered_set(data, names, headers):
    # 预编译正则表达式可以提高性能
    regex = re.compile("^\$\d+(\.\d+)?$")
    # 使用集合可以提高检索性能
    names_set = set(names)
    
    # 遍历数据，找到对应的 html_url，进行处理和过滤
    result_set = {s for item in data for s in fetch_and_parse(item["html_url"], headers, regex, names_set)}

    return result_set

def fetch_and_parse(url, headers, regex, names_set):
    page_content = get_response(url, headers)
    soup = BeautifulSoup(page_content, 'lxml')
    # 找到所有文本
    for s in soup.stripped_strings:
        s = " ".join(s.split())
        # 跳过不符合条件的字符串
        if (not s or
            s.isdigit() or
            regex.match(s) or
            s in names_set or
            re.search("\d+% OFF", s) or   # Add this line to skip strings containing "% OFF"
            any(unicodedata.category(c).startswith('Lo') for c in s)): # Add this line to filter Chinese characters
            continue
        yield s

result_set = get_filtered_set(data, names, headers)

log_list = [] # to hold logs
# 存储不在文件内的结果
not_found = []
found = []

# 对比result_set和compare_file
for file_url in outputInfo["compare_file"]:
    response = requests.get(file_url)
    data = json.loads(response.text)
    for item in result_set:
        if item not in found and item in data.values():
            found.append(item)
            log_list.append(f'文案“{item}”在文件“{file_url}”存在，且key为{list(data.keys())[list(data.values()).index(item)]}。')
        else:
            if item not in not_found and item not in found:
                not_found.append(item)

# 在公共多语言文件里面存在的值，则去掉
for v in not_found:
    if v in found:
        not_found.remove(v)  
print(not_found)

# # Save logs
with open(outputInfo['file_name'] + '_log.txt', 'w') as f:
    for log in log_list:
        f.write("%s\n" % log)

# 输出not_found到excel
df = pd.DataFrame(not_found, columns=['文案'])
df['文案长度'] = df['文案'].str.len()
df.to_excel(outputInfo['file_name'] + '.xlsx', index=False)
 
print('--------------end------------------')
# 打印结果
# for s in result_set:
#     print(s)