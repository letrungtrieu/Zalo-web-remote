from zalo import Zalo
import json
import os,sys,requests,subprocess

__version__ = "1.0.2"
DETACHED_PROCESS = 0x00000008

def read_str():
    fd = sys.stdin.fileno()
    input = os.read(fd,1024)
    return input.replace(b'\r\n',b'').decode('utf-8')

def kill_all_chrome():
    os.system('taskkill /f /im chrome.exe')
    os.system('taskkill /f /im python.exe')
    os.system('cls' if os.name=='nt' else 'clear')

def start():
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
        t = zalo.start()
    
    for t in zalos:
        t.join()
        
def check_update():
    res = requests.get("http://zalo.dichvugame.org/download/version.txt")
    version = res.content.decode()
    
    if __version__ != version and res.status_code == 200:
        subprocess.Popen(f"timeout 5 && curl -o Zalo.exe http://zalo.dichvugame.org/download/Zalo_{version}.exe", shell=True, creationflags=DETACHED_PROCESS)
        return False
    return True
        

if __name__=='__main__':
    if check_update():
        start()