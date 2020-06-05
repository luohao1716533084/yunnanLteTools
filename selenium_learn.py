#coding:utf-8

from selenium import webdriver
from tomorrow import threads
import pandas
import os


URL = "http://10.174.240.17:8081/portal/pure/Frame.action"

@threads(5)
def startBrowser(url):
    browser = webdriver.Chrome()                         #驱动浏览器
    browser.get(url)
    input_username = browser.find_element_by_id("username")
    input_username.send_keys("km_hw_shaoguohua")
    input_password = browser.find_element_by_id("password")
    input_password.send_keys("Password11!")
    button = browser.find_element_by_class_name("btn-submit")
    button.click()
    button_sys_notice = browser.find_element_by_class_name("sys-window-btn-close")
    button_sys_notice.click()

def get_receive_num():
    path = os.getcwd()
    dirs = os.listdir(path)
    """
    找到EUtranCellTDD, EUtranReselectionTDD文件路径，添加至file_file
	"""
    file_path = []
    for i in dirs:
        if "接单" in i:
            file_path.append(i)

if __name__ == '__main__':
    for i in range(5):
        startBrowser(URL)