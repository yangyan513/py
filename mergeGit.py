import git
from git.exc import GitCommandError
from colorama import Fore, Style, init
import os

init(autoreset=True)  # 将颜色设置回默认颜色

project_branches_list = [
    {"name": "/Users/yangyan/work/dvdfab_web", "branches": ["master", "pre1", "pre2","pre3","pre4","pre5", "pre9"]},
    {"name": "/Users/yangyan/work/images", "branches": ["master", "pre1", "pre2","pre3","pre4","pre5","pre9"]},
    {"name": "/Users/yangyan/work/images_us", "branches": ["master", "pre1", "pre2","pre3"]},
    {"name": "/Users/yangyan/work/dvdfab.us", "branches": ["master", "pre1", "pre2","pre3"]},
    {"name": "/Users/yangyan/work/dvdfab.us/static/locales", "branches": ["master", "pre1", "pre2","pre3"]},
    {"name": "/Users/yangyan/work/ja.dvdfab.cn", "branches": ["master", "pre1", "pre2","pre3"]},
    {"name": "/Users/yangyan/work/ura.dvdfab.org", "branches": ["master", "pre1", "pre2","pre3"]},
    {"name": "/Users/yangyan/work/ja.dvdfab.cn/static/locales", "branches": ["master", "pre1", "pre2","pre3"]},
    {"name": "/Users/yangyan/work/streamfab_us/static/locales", "branches": ["master", "pre1", "pre2","pre3","pre4","pre5","pre6"]},
    {"name": "/Users/yangyan/work/streamfab_us", "branches": ["master", "pre1", "pre2","pre3","pre4","pre5","pre6"]},
    {"name": "/Users/yangyan/work/streamfab_us/static/locales", "branches": ["master", "pre1", "pre2","pre3","pre4","pre5","pre6"]},
    {"name": "/Users/yangyan/work/dvdfab_web/static/locales", "branches": ["master", "pre1", "pre2","pre3","pre4","pre5","pre9"]},
    {"name": "/Users/yangyan/work/musicfab_web_new", "branches": ["master", "pre1", "pre2","pre3","pre4","pre5","pre6"]},
    {"name": "/Users/yangyan/work/musicfab_web_new/static/locales", "branches": ["master", "pre1", "pre2","pre3","pre4","pre5","pre6"]},
    {"name": "/Users/yangyan/work/ase_web", "branches": ["master", "pre1"]},
]

merge_list = [
    # {"project": "/Users/yangyan/work/images", "from": "master"},
    # {"project": "/Users/yangyan/work/images_us", "from": "pre1"},
    # {"project": "/Users/yangyan/work/dvdfab.us", "from": "pre2"},
    # {"project": "/Users/yangyan/work/dvdfab.us", "from": "pre1"},
    # {"project": "/Users/yangyan/work/dvdfab.us/static/locales", "from": "pre2"},
    # {"project": "/Users/yangyan/work/ja.dvdfab.cn", "from": "pre1"},
    # {"project": "/Users/yangyan/work/ja.dvdfab.cn", "from": "pre2"},
    # {"project": "/Users/yangyan/work/ja.dvdfab.cn", "from": "pre3"},
    # {"project": "/Users/yangyan/work/ja.dvdfab.cn/static/locales", "from": "pre3"},
    {"project": "/Users/yangyan/work/dvdfab_web", "from": "pre1"},
    # {"project": "/Users/yangyan/work/dvdfab_web", "from": "pre9"},
    # {"project": "/Users/yangyan/work/dvdfab_web/static/locales", "from": "pre5"},
    # {"project": "/Users/yangyan/work/dvdfab_web", "from": "pre2"},
    # {"project": "/Users/yangyan/work/streamfab_us", "from": "pre1"},
    # {"project": "/Users/yangyan/work/ura.dvdfab.org", "from": "pre3"},
    # {"project": "/Users/yangyan/work/streamfab_us/static/locales", "from": "pre1"},
    # {"project": "/Users/yangyan/work/streamfab_us", "from": "pre5"},
    # {"project": "/Users/yangyan/work/musicfab_web_new", "from": "master"},
    # {"project": "/Users/yangyan/work/musicfab_web_new", "from": "pre4"},
    # {"project": "/Users/yangyan/work/musicfab_web_new/static/locales", "from": "master"},
    # {"project": "/Users/yangyan/work/ase_web", "from": "pre1"},
]


def repo_exists(path):
    if not os.path.exists(path):
        return False
    return True


def merge_branches(repo, from_branch, to_branch):
    if from_branch == to_branch:
        print(f"[INFO] Branch names are the same on {repo}, skipping...")
        return
    try:
        repo.git.checkout(to_branch)
        repo.git.pull('origin', to_branch)
    except GitCommandError as e:
        print(Fore.RED + f"[ERROR] Checkout or pull for {to_branch} failed with error: {str(e)}")
        return
    try:
        repo.git.checkout(from_branch)
        repo.git.pull('origin', from_branch)
    except GitCommandError as e:
        print(Fore.RED + f"[ERROR] Checkout or pull for {from_branch} failed with error: {str(e)}")
        return
    try:
        repo.git.checkout(to_branch)
        merge_result = repo.git.merge(from_branch)
        if "Already up to date" in merge_result:
            print(f"[INFO] {from_branch} was already up to date with {to_branch}")
        else:
            print(Fore.GREEN + f"[SUCCESS] {from_branch} merged into {to_branch}")
        repo.git.push('origin', to_branch)
    except GitCommandError as e:
        print(Fore.RED + f"[ERROR] Merge failure on {to_branch} with {from_branch}: {str(e)}")
        repo.git.merge('--abort')


for project_merge_info in merge_list:
    project = project_merge_info["project"]
    from_branch = project_merge_info["from"]
    if repo_exists(project):
        repo = git.Repo(project)
        for project_info in project_branches_list:
            if project_info["name"] == project:
                for to_branch in project_info["branches"]:
                    merge_branches(repo, from_branch, to_branch)
    else:
        print(Fore.RED + f"[ERROR] Repository: {project} does not exist.")