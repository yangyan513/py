import os
import subprocess
from git import Repo, exc

def clone_repo(git_url, path, branches=None):
    if os.path.exists(path):
        print("Repository already exists at the specified path.")
        return

    subprocess.run(['git', 'clone', '--progress', git_url, path])
    if branches:
        repo = Repo(path)
        for branch in branches:
            try:
                repo.git.checkout(branch)
            except exc.GitCommandError:
                print(f"Branch '{branch}' does not exist in the repository.")


def install_packages(path):
    os.chdir(path)
    os.system('npm install')

projects = [
    {
        "mark": "",
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
        print(f"Cloning {project['webName']} repository...")
        clone_repo(project['webGit'], web_repo_path, project.get('branches'))
        print(f"Finished cloning {project['webName']} repository.")

    # Step 2. Clone the locales repositories
    for locale in project['locales']:
        locale_repo_path = os.path.join(web_repo_path, 'static', locale['name'])
        print(f"Cloning {locale['name']} repository...")
        clone_repo(locale['git'], locale_repo_path, locale.get('branches'))
        print(f"Finished cloning {locale['name']} repository.")

    # Step 3. Install packages
    if project['hasInstallPackages']:
        print(f"Installing packages for {project['webName']}...")
        install_packages(web_repo_path)
        print(f"Finished installing packages for {project['webName']}.")