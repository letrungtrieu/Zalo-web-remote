from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.support import expected_conditions as E
from threading import Thread
import os,time,re
from util import *



class Zalo(Thread):
    
    def __init__(self, tree, item_id, group_name: str, member_start_id: int, member_end_id: int, msg: str, sleep: float, profile):
        Thread.__init__(self)
        self.tree = tree
        self.item_id = item_id
        self.profile = profile
        self.chrome = None
        self.group_name = group_name
        self.member_index_id = int(member_start_id)
        self.member_index_stop_id = int(member_end_id)
        self.msg = msg
        self.sleep = float(sleep)
        self.is_stop = False

    def update(self, group_name: str, member_start_id: int, member_end_id: int, msg: str, sleep: float, profile):
        self.profile = profile
        self.chrome = None
        self.group_name = group_name
        self.member_index_id = int(member_start_id)
        self.member_index_stop_id = int(member_end_id)
        self.msg = msg
        self.sleep = float(sleep)
        self.is_stop = False
    
    def tree_update(self):
        values = self.tree.item(self.item_id)['values']
        values[1] = self.member_index_id + 1
        self.tree.item(self.item_id, values=values)
        save_config(self.tree)
    
    def get_options(self):
        options = Options()
        options.add_experimental_option(
            'excludeSwitches',
            ["enable-logging"]
        )
        options.add_argument(f'user-data-dir={os.getcwd()}\\profiles\\{self.profile}')
        options.binary_location = f'bin/chrome.exe'
        return options
    
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
                time.sleep(0.5)
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
                self.tree_update()
                time.sleep(self.sleep)
                break

    def stop(self):
        self.is_stop = True
        if self.chrome:
            self.chrome.quit()
        del self

    def run(self):
        chrome = webdriver.Chrome(service=Service(executable_path=f"chrome/chromedriver.exe"), options=self.get_options())
        chrome.get("https://zalo.me/zalo-chat")
        self.chrome = chrome
        self.wait_element = W(self.chrome, 120)
        
        while True:
            try:
                self.send_msg_for_member_of_group()
                self.member_index_id += 1
                if self.is_stop or self.member_index_id > self.member_index_stop_id:
                    print(f"Group {self.group_name} OK rồi nha ")
                    break
            except Exception as e:
                print(e)
                self.stop()
                break
                # print("Có lỗi xảy ra đang khởi động lại Chrome")
                # time.sleep(1)
                # if self.is_stop or self.member_index_id > self.member_index_stop_id:
                #     break
                # if self.chrome:
                #     self.chrome.quit()
                #     del self.chrome
                # self.chrome = webdriver.Chrome(service=Service(executable_path=f"chrome/chromedriver.exe"), options=self.get_options())
                # self.chrome.get("https://zalo.me/zalo-chat")
                # self.wait_element = W(self.chrome, 120)