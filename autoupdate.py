import shutil
import git
import os
import json
import tqdm

class GitCloneProgress(git.remote.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        if max_count is not None:
            progress_bar.total = max_count
            progress_bar.update(cur_count - progress_bar.n)

def first_run():
    if not os.path.exists(os.path.abspath('.') + "/config.json"):
        if not os.path.exists(os.path.abspath('.') + "/MAA.exe"):
            maa_path = input("填入MAA路径: ")
        else:
            maa_path = os.path.abspath('.') 
        work_path = os.path.abspath('.')
        config = {
            "repo_url": "https://gitee.com/balderdash1/MaaResource.git",
            "MAA_path": maa_path,
            "work_path": work_path
        }
        with open("config.json", "w") as f:
            json.dump(config, f)
        return True
    return False


if first_run():
    json_file = os.path.abspath('.') + "/config.json"
    with open(json_file, "r") as f:
        config = json.load(f)
    repo_url = config["repo_url"]   
    repo_path = config["work_path"] + "/MaaResource"
    progress_bar = tqdm.tqdm(total=100, unit='B', unit_scale=True)
    git.Repo.clone_from("https://gitee.com/balderdash1/MaaResource.git", repo_path, progress=GitCloneProgress())
    progress_bar.close()
    exit()
else:    
    with open("config.json", "r") as f:
        config = json.load(f)
    repo = git.Repo(config["work_path"] + "/MaaResource")
    diff = repo.git.diff('origin', 'HEAD~1')
    if diff != "":
        repo.remotes.origin.pull()
        src_dir_Resourse = config["work_path"] + "/MaaResource/Resource"
        src_dir_Cache = config["work_path"] + "/MaaResource/Cache"
        shutil.copytree(src_dir_Resourse, config["MAA_path"] + "/Resource", dirs_exist_ok=True)   
        shutil.copytree(src_dir_Cache, config["MAA_path"] + "/Cache", dirs_exist_ok=True) 
        print("Auto update success!")
    else:
        print("No update needed!")