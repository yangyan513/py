###
# pip install gitpython
# pip install python-dateutil
from git import Repo
from datetime import datetime
from functools import reduce
from dateutil import tz  # 新增的库

def list_changed_files_after_date_by_authors(repo_path, branch, authors, date):
    commit_authors = authors.split(',')
    date_obj = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    date_obj = date_obj.replace(tzinfo=tz.UTC)
    repo = Repo(repo_path)
    commits = list(repo.iter_commits(branch))
    changed_files = set()
    for commit in commits:
        
        if 'Merge' in commit.message:  # 加这一句
            continue
        if commit.authored_datetime >= date_obj and commit.author.name in commit_authors:
            for parent in commit.parents:
                diffs = parent.diff(commit)
                for diff in diffs.iter_change_type('M'):  # Modified files
                    changed_files.add(diff.a_path)
                for diff in diffs.iter_change_type('A'):  # Added files
                    changed_files.add(diff.a_path)
    return list(changed_files)


repo_path = "/Users/yangyan/work/dvdfab_web" # 你的本地git仓库路径
# repo_path = '/Users/yangyan/work/images'

branch = 'master' # 你的分支名
authors = '阳艳' # 提交者名称，用逗号分隔
date = '2023-09-11 00:17:00' # 开始日期时间

files = list_changed_files_after_date_by_authors(repo_path, branch, authors, date)
#############修改的文件
if len(files) == 0:
  print('---------------没有检测出修改的文件，可能是时间的配置需要往前推8个小时，或者更多--------------')
else:
  print('---------------复制的文件：')
  print(files)

#######################复制
import os
import shutil

# 初始化源文件夹
# source_folder_name = '/Users/yangyan/work/dvdfab_web'
source_folder_name = repo_path


# 初始化目标文件夹列表
##, '/Users/yangyan/work/dvdfab.us'
target_folder_names = ['/Users/yangyan/work/ja.dvdfab.cn', '/Users/yangyan/work/dvdfab.us', '/Users/yangyan/work/streamfab_us']
# target_folder_names = ['/Users/yangyan/work/images_us', '/Users/yangyan/work/streamfab_us/static']

# 初始化文件列表
file_list = files

# 循环处理每个目标文件夹
for target_folder_name in target_folder_names:

    # 循环处理文件
    for file_name in file_list:
        try:
            source_file = os.path.join(source_folder_name, file_name)
            target_file = os.path.join(target_folder_name, file_name)
            os.makedirs(os.path.dirname(target_file), exist_ok=True)

            r_ = shutil.copy2(source_file, target_file)
        except Exception as e:
            print(f"Error copying {source_file} to {target_file}: {e}")
if len(file_list) == 0:
  print("没有可复制的文件！")
else:
  print("复制完成!")
  print("代码提交之前，还是需要仔细review哟!")
