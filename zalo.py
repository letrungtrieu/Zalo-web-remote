from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.support import expected_conditions as E
from threading import Thread
import os,time,re



class Zalo(Thread):
    
    def __init__(self, user_path, proxy:str, group_name: str, member_index_id: int, member_index_stop_id: int, msg: str, sleep: float):
        Thread.__init__(self)
        self.profile = user_path
        self.options = Options()
        self.options.add_experimental_option(
            'excludeSwitches',
            ["enable-logging"]
        )
        self.options.binary_location = f'bin/chrome.exe'
        if proxy:
            self.options.add_argument(f'--proxy-server=http://{proxy}')
        self.options.add_argument(f'user-data-dir={os.getcwd()}\\profiles\\{user_path}')
        chrome = webdriver.Chrome(service=Service(executable_path=f"chrome/chromedriver.exe"), options=self.options)
        chrome.get("https://zalo.me/zalo-chat")
        self.chrome = chrome
        self.wait_element = W(self.chrome, 120)
        self.group_name = group_name
        self.member_index_id = member_index_id
        self.member_index_stop_id = member_index_stop_id
        self.msg = msg
        self.sleep = sleep
        self.is_stop = False

    def send_msg_for_member_of_group(self):
        print(f"------{self.profile}-------")
        search_input: list[WebElement] = self.wait_element.until(E.presence_of_all_elements_located((
            By.CSS_SELECTOR,
            "input#contact-search-input"
        )))
        search_input[0].click()
        search_input[0].send_keys(self.group_name)
        search_item: list[WebElement] = self.wait_element.until(E.presence_of_all_elements_located((
            By.CSS_SELECTOR,
            f'div[id*="group-item-g"]'
        )))
        search_item[0].click()

        num_member: list[WebElement] = self.wait_element.until(E.presence_of_all_elements_located((
            By.CSS_SELECTOR,
            "div.subtitle__groupmember__content.flx.flx-al-c.clickable"
        )))
        num_member[0].click()
        time.sleep(1)
        member_list: list[WebElement] = self.wait_element.until(E.presence_of_all_elements_located((
            By.CSS_SELECTOR,
            "div.chat-box-member__info__name.v2"
        )))

        while self.member_index_id < self.member_index_stop_id:
            name_el: WebElement = member_list[self.member_index_id].find_element(by=By.CSS_SELECTOR, value="div.truncate")
            name_member:str = name_el.text
            if not name_member:
                continue
            flag = re.search("Tài khoản bị khóa", name_member) or re.search("Account(.*)Banned", name_member)
            if flag:
                print(f"------STT   {self.member_index_id}-------")
                print("------Tài khoản bị khóa-----")
                print("----------------------------------------------------------------")
                self.member_index_id +=1
            else:
                print(">>>>>>Gửi tin nhắn cho ", name_member)
                member_list[self.member_index_id].click()
                btn_msg: list[WebElement] = self.wait_element.until(E.presence_of_all_elements_located((
                    By.CSS_SELECTOR,
                    'div[data-translate-inner="STR_CHAT"]'
                )))
                btn_msg[0].click()
                time.sleep(2)
                send_msg: list[WebElement] = self.wait_element.until(E.presence_of_all_elements_located((
                    By.CSS_SELECTOR,
                    "div#input_line_0"
                )))
                send_msg[0].send_keys(self.msg)
                time.sleep(1)
                qick_message: list[WebElement] = self.wait_element.until(E.presence_of_all_elements_located((
                                    By.CSS_SELECTOR,
                                    'div[class="qri clickable active"]'
                                )))
                time.sleep(3)
                qick_message[0].click()
                time.sleep(3)
                btn_send_msg: list[WebElement] = self.wait_element.until(E.presence_of_all_elements_located((
                    By.CSS_SELECTOR,
                    'div[data-translate-inner="STR_SEND"]'
                )))
                btn_send_msg[0].click()
                print(f"------STT   {self.member_index_id}-------")
                print("------Đã gửi thành công-----")
                print("----------------------------------------------------------------")
                time.sleep(self.sleep)
                break
        
        
        

    def stop(self):
        self.is_stop = True
        self.chrome.close()
        del self

    def run(self):
        while True:
            # try:
            self.send_msg_for_member_of_group()
            self.member_index_id += 1
            if self.is_stop or self.member_index_id > self.member_index_stop_id:
                print(f"Group {self.group_name} OK rồi nha ")
                break
            # except Exception as e:
            #     print(e)
            #     print("Có lỗi xảy ra đang khởi động lại Chrome")
            #     time.sleep(10)
            #     self.chrome.quit()
            #     del self.chrome
            #     self.chrome = webdriver.Chrome(f"{os.getcwd()}\\chrome\\chromedriver.exe", options=self.options)
            #     self.chrome.get("https://zalo.me/zalo-chat")
            #     self.wait_element = W(self.chrome, 120)