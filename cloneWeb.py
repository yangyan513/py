import os
from git import Repo

def clone_repo(git_url, path):
    Repo.clone_from(git_url, path)

def install_packages(path):
    os.chdir(path)
    os.system('npm install')

projects = [
    {
        "mark": ""
        "dir": "/Users/yangyan/work",
        "hasClone": 1,
        "hasInstallPackages": 1,
        "webGit": "",
        "webName": "",
        "locales": [
            {
                "git": "",
                "name": ""
            }
        ]
    }
]

for project in projects:
    # Step 1. Clone the webGit repository
    web_repo_path = os.path.join(project['dir'], project['webName'])
    if project['hasClone']:
        clone_repo(project['webGit'], web_repo_path)

    # Step 2. Clone the locales repositories
    for locale in project['locales']:
        locale_repo_path = os.path.join(web_repo_path, 'static', locale['name'])
        clone_repo(locale['git'], locale_repo_path)

    # Step 3. Install packages
    if project['hasInstallPackages']:
        install_packages(web_repo_path)