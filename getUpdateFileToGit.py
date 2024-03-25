###
# pip install gitpython
# pip install python-dateutil
from git import Repo
from datetime import datetime
from functools import reduce
from dateutil import tz

def list_changed_files_after_date_by_authors(repo_path, branch, authors, start_date, end_date):
    commit_authors = authors.split(',')
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S').replace(tzinfo=tz.UTC)
    if end_date == '':
        end_date_obj = datetime.now().replace(tzinfo=tz.UTC)
    else:
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S').replace(tzinfo=tz.UTC)
    
    repo = Repo(repo_path)
    commits = list(repo.iter_commits(branch))
    
    changed_files = set()
    deleted_files = []  # 用于记录被删除的文件路径
    
    for commit in commits:
        if 'Merge' in commit.message:
            continue
        
        if start_date_obj <= commit.authored_datetime <= end_date_obj and commit.author.name in commit_authors:
            for parent in commit.parents:
                diffs = parent.diff(commit)
                for diff in diffs:
                    if diff.change_type in ['M', 'A']:  # Modified, Added files
                        changed_files.add(diff.a_path)
                    if diff.change_type in ['R']:  # Renamed files
                        changed_files.add(diff.b_path)
                    elif diff.change_type == 'D':  # Deleted files
                        changed_files.add(diff.a_path)  # 将被删除的文件名也放入 changed_files 中
                        deleted_files.append(diff.a_path)  # 记录被删除的文件路径
    
    return list(changed_files), deleted_files


# repo_path = "D:\work\images"  # 你的本地git仓库路径
repo_path = "D:\work\dvdfab_web"  # 你的本地git仓库路径
# repo_path = "D:\work\streamfab.us"  # 你的本地git仓库路径
branch = 'pre6'  # 你的分支名
branch = 'master'  # 你的分支名
authors = '姚飞扬,秦陈志'  # 提交者名称，用逗号分隔
# authors = '韩钊,姚飞扬,秦陈志'  # 提交者名称，用逗号分隔
authors = '阳艳'  # 提交者名称，用逗号分隔
start_date = '2024-03-25 00:00:00'  # 开始日期时间
end_date = ''#'2024-02-27 00:00:00'  # 结束日期时间

files, deleted_files = list_changed_files_after_date_by_authors(repo_path, branch, authors, start_date, end_date)

if len(files) == 0:
    print('---------------没有检测出修改的文件--------------')
else:
    print('---------------修改的文件：')
    print(files)

if len(deleted_files) == 0:
    print('---------------没有检测出删除的文件--------------')
else:
    print('---------------被删除的文件：')
    print(deleted_files)




#######################复制
import os
import shutil

# 初始化源文件夹
source_folder_name = repo_path


# 初始化目标文件夹列表
target_folder_names = ['D:\work/dvdfab_web']
target_folder_names = [ 'D:\work/dvdfab.org']
# target_folder_names = [ 'D:\work/dvdfab.org','D:\work/dvdfab.us', 'D:\work/streamfab.us']
# target_folder_names = ['D:\work/ja.dvdfab.cn', 'D:\work/dvdfab.us', 'D:\work/streamfab.us', 'D:\work/ura.dvdfab.org', 'D:\work/dvdfab.org','D:\work/dvdfab_web']
# target_folder_names = ['D:\work/images_us', 'D:\work/streamfab.us/static']
# target_folder_names = ['D:\work/streamfab.us/static']
# target_folder_names = ['D:\work/images1']

# 初始化文件列表
file_list = files

# 循环处理每个目标文件夹
for target_folder_name in target_folder_names:

    # 循环处理文件
    for file_name in file_list:
        try:
            target_file_name = file_name
            if 'streamfab' in target_folder_name and 'pages' in target_file_name:
               target_file_name = file_name.replace('pages', 'pages/main')
            # 主站同步到streamfab，目录加上pages
            if 'streamfab' in target_folder_name and 'pages' in target_file_name:
               target_file_name = file_name.replace('pages', 'pages/main')
            #streamfab 站的promotion_info同步到主站目录去掉main
            if 'streamfab' in source_folder_name and 'pages' in file_name:
               target_file_name = file_name.replace('pages/main', 'pages')
            # streamfab 站的promotion_info同步到主站改名
            if 'streamfab' in source_folder_name and 'promotion/promotion_info' in file_name:
               target_file_name = file_name.replace('promotion_info', 'streamfab_promotion_info')  
            # streamfab 站的图片同步到主站去掉static
            if 'images' in target_folder_name and 'static/' in file_name:
               target_file_name = file_name.replace('static/', '')
            # 非图片目录不同步
            if 'images' in target_folder_name and not target_file_name.startswith(("images", "webp")):
               continue
            # streamfab站的代码同步到主站忽略图片
            if 'dvdfab' in target_folder_name and target_file_name.startswith(("static/images", "static/webp")):
               continue
            source_file = os.path.join(source_folder_name, file_name)
            target_file = os.path.join(target_folder_name, target_file_name)
            os.makedirs(os.path.dirname(target_file), exist_ok=True)

            r_ = shutil.copy2(source_file, target_file)
        except Exception as e:
            print(f"Error copying {source_file} to {target_file}: {e}")
if len(file_list) == 0:
  print("没有可复制的文件！")
else:
  print("复制完成!")
  print("代码提交之前，还是需要仔细review哟!")


import os
from colorama import init, Fore  # 使用colorama库进行彩色输出

init(autoreset=True)  # 初始化colorama，autoreset参数用于自动重置颜色

def delete_files_in_folders(target_folders, files_to_delete):
    success = True

    for folder_name in target_folders:
        for file_name in files_to_delete:
            file_path = os.path.join(folder_name, file_name)
            try:
                os.remove(file_path)
                print(f"成功删除文件: {file_path}")
            except OSError as e:
                success = False
                print(Fore.RED + f"删除文件失败: {file_path}")

    return success

success = delete_files_in_folders(target_folder_names, deleted_files)

if success:
    print("所有文件删除成功！")
else:
    print("部分文件删除失败，请检查输出信息。")
