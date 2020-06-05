#coding:utf-8

from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

url = "http://10.174.240.17:8081/portal/pure/Frame.action"

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

# 选择在线协作
# zaixianxiezuo = browser.find_element_by_xpath('//*[@id="node_ZXXZ"]/i')
# zaixianxiezuo.click()

#定位到要双击的元素
qqq =browser.find_element_by_xpath('//*[@id="node_ZXXZ"]/i')
#对定位到的元素执行鼠标双击操作
ActionChains(browser).double_click(qqq).perform()



# 中端优化市到三方
browser.switch_to.frame("link1")


time.sleep(5)                                                                                                          #强制睡眠10s
move = browser.find_element_by_xpath('/html/body/div[1]/div/div/div')
ActionChains(browser).move_to_element(move).perform()
input_gongdanNum = browser.find_element_by_xpath('//*[@id="public_inputCompinent__inputMainorderCode"]')                #定位工单号输入框
input_gongdanNum.send_keys("ZDYH-KM-CG064-20200511-01857432")                                                           #输入工单号


search_gongdan = browser.find_element_by_id('task_management_mat')                  #定位工单搜索框
search_gongdan.click()                                                              #点击搜索框

# 任务处理


time.sleep(5)
# 操作按钮
data = browser.find_element_by_class_name("tableDropdown")
data.click()

#任务处理
taskProcButton = browser.find_element_by_xpath('/html/body/ul/div[2]/li/i')
taskProcButton.click()

dataTime = browser.find_element_by_xpath('//*[@class="el-tabs__nav-scroll"]/div')