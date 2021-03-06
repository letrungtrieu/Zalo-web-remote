from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.support import expected_conditions as E
from threading import Thread
import os,time



class Zalo(Thread):
    
    def __init__(self, user_path, proxy:str, group_name: str, group_id: str, member_index_id: int, member_index_stop_id: int, msg: str, sleep: float):
        Thread.__init__(self)
        self.options = Options()
        self.options.add_experimental_option(
            'excludeSwitches',
            ["enable-logging"]
        )
        if proxy:
            self.options.add_argument(f'--proxy-server=http://{proxy}')
        self.options.add_argument(f'user-data-dir={user_path}')
        self.chrome = webdriver.Chrome(f"{os.getcwd()}\\chrome\\chromedriver.exe", options=self.options)
        self.chrome.get("https://zalo.me/zalo-chat")
        self.wait_element = W(self.chrome, 120)
        self.group_name = group_name
        self.group_id = group_id
        self.member_index_id = member_index_id
        self.member_index_stop_id = member_index_stop_id
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
            print(">>>>>>G???i tin nh???n cho ", name_el.text)
        except:
            pass
        member_list[self.member_index_id].click()

        btn_msg: list[WebElement] = self.wait_element.until(E.presence_of_all_elements_located((
            By.CSS_SELECTOR,
            'div[data-id="btn_UserProfile_SendMsg"]'
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
            if self.is_stop or self.member_index_id == self.member_index_stop_id:
                break
            try:
                self.send_msg_for_member_of_group()
                print(f"------STT   {self.member_index_id}-------")
                print("------???? g???i th??nh c??ng-----")
                print("----------------------------------------------------------------")
                self.member_index_id += 1
                time.sleep(self.sleep)
            except Exception as e:
                print("C?? l???i x???y ra ddang kh???i ?????ng l???i Chrome")
                time.sleep(10)
                self.chrome.quit()
                del self.chrome
                self.chrome = webdriver.Chrome(f"{os.getcwd()}\\chrome\\chromedriver.exe", options=self.options)
                self.chrome.get("https://zalo.me/zalo-chat")
                self.wait_element = W(self.chrome, 120)