#coding:utf-8

"""
selenium 基本操作
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

brower = webdriver.Chrome()

try:
    brower.get("https://www.baidu.com")
    input = brower.find_element_by_id("kw")                     #kw应该是收缩框
    input.send_keys("python")
    input.send_keys(Keys.ENTER)
    wait = WebDriverWait(brower, 10)
    wait.until(EC.presence_of_element_located((By.ID, "content_left")))
    print(brower.current_url)
    print(brower.get_cookies())
    print(brower.page_source)
finally:
    brower.close()

"""
声明浏览器对象
from selenium import webdriver

browser = webdriver.Chrome()
browser = webdriver.Firefox()
browser = webdriver.Edge()
browser = webdriver.PhantomJS()
browser = webdriver.Safari()
"""

"""
访问页面
from selenium import 

"""

