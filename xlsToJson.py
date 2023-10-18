import pandas as pd
import openpyxl
import json

# 读取Excel文件
df = pd.read_excel(r'D:\work\py\key_not_use_vue_json_dvdfab.cn_master.xlsx')

# 创建字典用于存储数据
data = {}

# 遍历每个sheet
for sheet_name in df.keys():
    # 筛选当前sheet的数据
    sheet_data = df[df['file'] == sheet_name]['key'].tolist()

    # 将数据存储到字典中
    if sheet_name in data:
        data[sheet_name].extend(sheet_data)
    else:
        data[sheet_name] = sheet_data

# 生成JSON文件
with open('output.json', 'w') as f:
    json.dump(data, f)