#coding:utf-8

from selenium import webdriver

url = "http://10.174.240.17:8081/portal/pure/Frame.action"

browser = webdriver.Chrome()
browser.get(url)
input_username = browser.find_element_by_id("username")
input_username.send_keys("hechunfen")
input_password = browser.find_element_by_id("password")
input_password.send_keys("hechunfen0304")
button = browser.find_element_by_class_name("btn-submit")
button.click()

button_sys_notice = browser.find_element_by_class_name("sys-window-btn-close")
button_sys_notice.click()