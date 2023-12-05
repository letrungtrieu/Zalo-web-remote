from zalo import Zalo
import json
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
        for dir in list(configs.keys()):
            config = configs[dir]
            group_name=config["groupName"]
            index_start_member=config["memberId"]
            index_stop_member=config["memberEndId"]
            message=config["msg"]
            time_sleep=config["delay"]
            proxy = config["proxy"]
            zalos.append(Zalo(dir, proxy, group_name, index_start_member, index_stop_member, message, time_sleep))
    
    for zalo in zalos:
        zalo.start()
        zalo.join()