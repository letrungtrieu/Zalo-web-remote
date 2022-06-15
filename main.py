from zalo import Zalo
import json, zipfile
import os,sys

def read_str():
    fd = sys.stdin.fileno()
    input = os.read(fd,1024)
    return input.replace(b'\r\n',b'').decode('utf-8')

def kill_all_chrome():
    os.system('taskkill /f /im chrome.exe')
    os.system('taskkill /f /im python.exe')
    os.system('cls' if os.name=='nt' else 'clear')

if __name__=='__main__':
    zalos:list[Zalo] = []

    with open('config.json',  encoding='utf-8') as f:
        file = f.read()
        configs:dict = json.loads(file)
        pc = list(configs.keys())[0]
        configs = configs[pc]
        for dir in list(configs.keys()):
            if not os.path.exists(f'C:\\Users\\{pc}\\AppData\\Local\\Google\\Chrome\\{dir}'):
                zipfile.ZipFile('chrome/User Data.zip').extractall(f'C:\\Users\\{pc}\\AppData\\Local\\Google\\Chrome\\{dir}')
            
            config = configs[dir]
            group_name=config["groupName"]
            group_id=config["groupId"]
            index_start_member=config["memberId"]
            index_stop_member=config["memberEndId"]
            message=config["msg"]
            time_sleep=config["delay"]
            proxy = config["proxy"]
            zalos.append(Zalo(f'C:\\Users\\{pc}\\AppData\\Local\\Google\\Chrome\\{dir}\\User Data', proxy, group_name, group_id, index_start_member, index_stop_member, message, time_sleep))
    
    for zalo in zalos:
        zalo.start()