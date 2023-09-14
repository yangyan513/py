import glob
import os
import json

# 从目录中查找所有.vue文件
vue_files = glob.glob('/Users/yangyan/work/dvdfab_web/pages/**/*.vue', recursive=True)

# 创建一个空集合用于保存不重复的文件名
unique_filenames = set()

for vue_file in vue_files:
    # 获取文件的文件名
    filename = os.path.basename(vue_file).split('.')[0]
    # 获取文件的父目录名
    parent_dir = os.path.basename(os.path.dirname(vue_file))

    # 父文件地址不为pages, 且文件名为index的情况 或 文件名_开头的
    if parent_dir != 'pages' and (filename == 'index' or filename.startswith('_')):
        unique_filenames.add(parent_dir + '.json')
    else:
        unique_filenames.add(filename + '.json')

# 将集合转换为列表
unique_filenames = list(unique_filenames)

# 打印结果，或者在需要的地方使用结果
print(unique_filenames)
print(len(unique_filenames))

### 除了和文件名一致的文件，还需要哪些文件
import requests
import json

res = requests.get('https://example.com/config/i18n/i18n.json')
data = res.json()

def get_need_values(d):
    for k, v in d.items():
        if k == 'need':
            for item in v:
                need_values.add(item + '.json')
        elif isinstance(v, dict):
            get_need_values(v)

need_values = set()
get_need_values(data)
need_values = list(need_values)
print(need_values)

### 在使用的多语言文件
import numpy as np
toolkit = ['video_to_gif.json',
    'video_to_jpg.json',
    'image_to_video.json',
    'gif_to_video.json',
    'add_text_to_video.json',
    'timestamp.json',
    'add_image_to_video.json',
    'add_subtitles_to_video.json',
    'extract_subtitles.json',
    'mp3_converter.json',
    'audio_trimmer.json',
    'pump_up_the_volume.json',
    'denoise.json',
    'normalize_audio.json',
    'audio_merger.json',
    'audio_extractor.json',
    'remux_audio.json',
    'convert_video.json',
    'video_trimmer.json',
    'speed_up_video.json',
    'flip_video.json',
    'rotate_video.json',
    'crop_video.json',
    'sharpen_video.json',
    'video_stabilizer.json',
    'video_merger.json',
    'remove_audio_from_video.json',
    'deinterlace.json',
    'toolkit_public_page.json',]
files = ['index.json','common.json', 'recom_desc.json', 'promotion_1.json', 'promotion_2.json', 'promotion_3.json']
json_files = np.concatenate((unique_filenames, need_values, files,toolkit))


import pandas as pd

# 开启excel文件
excel_file = pd.ExcelFile('/Users/yangyan/work/py/lang_key_not_use_file_key_dvdfab.cn_master_en.xls')

# 定义一个空的集合，用于存放所有的G列的去重值
unique_values = set()

# 遍历所有的表单
for sheet in excel_file.sheet_names:
    # 读取单个表单的数据
    df = excel_file.parse(sheet)
    
    # 检查是否存在'file'列
    if 'file' in df.columns:
    
        # 遍历G列的值
        for value in df['file']:
            # 添加到集合中，实现去重
            unique_values.add(value + '.json')
    else:
        print(f"No column 'file' in sheet: {sheet}")

# 转换集合为列表并输出
unique_values_list = list(unique_values)
print(unique_values_list)
print(len(unique_values_list))


# 根据题目要求，需要找出在sheet_names_json中但不在json_files中的元素
result = list(set(unique_values_list) - set(json_files))

# 对结果进行升序排序
result.sort()
print(result)

