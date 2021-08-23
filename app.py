from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.support import expected_conditions as E
from selenium.webdriver import ActionChains as A
import sys


options = Options()
options.add_experimental_option(
    'excludeSwitches',
    ['disable-sync']
)
options.add_argument('--enable-sync')
options.add_argument(
    f'user-data-dir=c:/Users/{sys.argv[1]}/AppData/Local/Google/Chrome/User Data/'
)
chrome = webdriver.Chrome("chromedriver.exe", options=options)
chrome.get("https://zalo.me/zalo-chat")

wait_element = W(chrome, 120)
action = A(chrome)


def send_msg_for_member_of_group(group_name, group_id, index_member, msg):

    search_input: list[WebElement] = wait_element.until(E.presence_of_all_elements_located((
        By.CSS_SELECTOR, 
        "input#contact-search-input"
    )))
    search_input[0].click()
    search_input[0].send_keys(group_name)
    search_item: list[WebElement] = wait_element.until(E.presence_of_all_elements_located((
        By.CSS_SELECTOR,
        f"div#group-item-g{group_id}"
    )))
    search_item[0].click()

    num_member: list[WebElement] = wait_element.until(E.presence_of_all_elements_located((
        By.CSS_SELECTOR,
        "div.subtitle__groupmember__content.flx.flx-al-c.clickable"
    )))
    num_member[0].click()

    member_list: list[WebElement] = wait_element.until(E.presence_of_all_elements_located((
        By.CSS_SELECTOR,
        "div.chat-box-member__info__name.v2"
    )))
    try:
        name_el: WebElement = member_list[index_member].find_element_by_css_selector(
            "div.truncate")
        print(">>>>>>Gửi tin nhắn cho ", name_el.text)
    except:
        pass
    member_list[index_member].click()

    btn_msg: list[WebElement] = wait_element.until(E.presence_of_all_elements_located((
        By.CSS_SELECTOR,
        "div.user-profile-button.lf"
    )))
    btn_msg[0].click()

    send_msg: list[WebElement] = wait_element.until(E.presence_of_all_elements_located((
        By.CSS_SELECTOR,
        "div#input_line_0"
    )))
    send_msg[0].send_keys(msg)

    btn_send_msg: list[WebElement] = wait_element.until(E.presence_of_all_elements_located((
        By.CSS_SELECTOR,
        "div.z--btn.z--btn--text--primary.-lg.--rounded.send-btn-chatbar.input-btn"
    )))
    btn_send_msg[0].click()
    print("------Đã gửi thành công-----")
    print("----------------------------------------")


def run(group_name:str, group_id:str, member_index_id: int, msg:str):
    while True:
        send_msg_for_member_of_group(
            group_name,
            group_id,
            member_index_id,
            msg
        )
        member_index_id += 1


if __name__ == '__main__':
    run(sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5])
