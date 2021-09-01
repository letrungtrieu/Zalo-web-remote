from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.support import expected_conditions as E
from threading import Thread
from glob import glob
import sys,os,time,json



class Zalo(Thread):
    
    def __init__(self, group_name: str, group_id: str, member_index_id: int, msg: str, sleep: float):
        Thread.__init__(self)
        self.options = Options()
        self.options.add_experimental_option(
            'excludeSwitches',
            ["enable-logging"]
        )
        for user in glob('c:/users/*'):
            user_path = f'{user}/AppData/Local/Google/Chrome/User Data/'
            if os.path.isdir(user_path):
                self.options.add_argument(f'user-data-dir={user_path}')
                break
        
        self.chrome = webdriver.Chrome(f"{os.getcwd()}\\chromedriver.exe", options=self.options)
        self.chrome.get("https://zalo.me/zalo-chat")
        self.wait_element = W(self.chrome, 45)
        self.group_name = group_name
        self.group_id = group_id
        self.member_index_id = member_index_id
        self.msg = msg
        self.sleep = sleep
        self.is_stop = False

    def send_msg_for_member_of_group(self):

        search_input: list[WebElement] = self.wait_element.until(E.presence_of_all_elements_located((
            By.CSS_SELECTOR,
            "input#contact-search-input"
        )))
        search_input[0].click()
        search_input[0].send_keys(self.group_name)
        search_item: list[WebElement] = self.wait_element.until(E.presence_of_all_elements_located((
            By.CSS_SELECTOR,
            f"div#group-item-g{self.group_id}"
        )))
        search_item[0].click()

        num_member: list[WebElement] = self.wait_element.until(E.presence_of_all_elements_located((
            By.CSS_SELECTOR,
            "div.subtitle__groupmember__content.flx.flx-al-c.clickable"
        )))
        num_member[0].click()

        member_list: list[WebElement] = self.wait_element.until(E.presence_of_all_elements_located((
            By.CSS_SELECTOR,
            "div.chat-box-member__info__name.v2"
        )))
        try:
            name_el: WebElement = member_list[self.member_index_id].find_element_by_css_selector(
                "div.truncate")
            print(">>>>>>Gửi tin nhắn cho ", name_el.text)
        except:
            pass
        member_list[self.member_index_id].click()

        btn_msg: list[WebElement] = self.wait_element.until(E.presence_of_all_elements_located((
            By.CSS_SELECTOR,
            "div.user-profile-button.lf"
        )))
        btn_msg[0].click()

        send_msg: list[WebElement] = self.wait_element.until(E.presence_of_all_elements_located((
            By.CSS_SELECTOR,
            "div#input_line_0"
        )))
        send_msg[0].send_keys(self.msg)

        btn_send_msg: list[WebElement] = self.wait_element.until(E.presence_of_all_elements_located((
            By.CSS_SELECTOR,
            "div.z--btn.z--btn--text--primary.-lg.--rounded.send-btn-chatbar.input-btn"
        )))
        btn_send_msg[0].click()

    def stop(self):
        self.is_stop = True
        self.chrome.close()
        del self

    def run(self):
        while True:
            if self.is_stop:
                break
            try:
                self.send_msg_for_member_of_group()
                print(f"------STT   {self.member_index_id}-------")
                print("------Đã gửi thành công-----")
                print("----------------------------------------------------------------")
                self.member_index_id += 1
                time.sleep(self.sleep)
            except Exception as e:
                kill_all_chrome()
                self.chrome = webdriver.Chrome("chromedriver.exe", options=self.options)
                self.chrome.get("https://zalo.me/zalo-chat")
                self.wait_element = W(self.chrome, 45)

def read_str():
    fd = sys.stdin.fileno()
    input = os.read(fd,1024)
    return input.replace(b'\r\n',b'').decode('utf-8')

def get_info():
    os.system('cls' if os.name=='nt' else 'clear')
    try:
        print("Nhập đường dẫn đến file json:")
        with open('config.json',  "r") as f:
            file = f.read()
            config = json.loads(file)
            group_name=config["groupName"]
            group_id=config["groupId"]
            index_member=config["memberId"]
            message=config["msg"]
            time_sleep=config["delay"]
            return (group_name, group_id, index_member, message, time_sleep)
    except Exception as e:
        print("Không tìm thấy file, hoặc định dạng sai! Ấn enter để tiếp tục!", e)
        read_str()
        get_info()

def kill_all_chrome():
    os.system('taskkill /f /im chrome.exe')
    os.system('cls' if os.name=='nt' else 'clear')

if __name__ == '__main__':
    while True:
        group_name, group_id, index_member, message, time_sleep = get_info()
        kill_all_chrome()
        zalo = Zalo(group_name, group_id, index_member, message, time_sleep)
        zalo.start()
        read_str()
        zalo.stop()
        break
        
