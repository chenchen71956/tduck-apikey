#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.edge.options import Options

edge_options = Options()
edge_options.add_argument('--headless')  # 启用无头模式
edge_options.add_argument('--ignore-certificate-errors')
edge_options.add_argument('--ignore-ssl-errors')

try:
    driver = webdriver.Edge(options=edge_options)
except WebDriverException as e:
    print(f"Failed to initialize WebDriver: {e}")
    exit(1)

def login_to_backend(driver):
    """
    通过selenium模拟登录，获取API Key
    :return: API Key
    """
    try:
        driver.get('http://bot.cynasck.asia:8999/project/form/setting?key=hlYd7ZZQ')  # 替换为实际的后台登录URL
        driver.maximize_window()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="text"]'))
        )
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="password"]'))
        )
        print("登录成功，等待获取key...")
        username_input.send_keys('admin@tduckcloud.com')  # 替换为实际的用户名
        password_input.send_keys('123456')  # 替换为实际的密码
        password_input.send_keys(Keys.RETURN)
        api_key_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-immersive-translate-walked]'))
        )
        api_key = api_key_element.get_attribute('data-immersive-translate-walked')
        return api_key
    except (TimeoutException, WebDriverException) as e:
        return None

def click_element(driver, css_selector):
    """
    点击指定CSS选择器的元素
    :param driver: WebDriver实例
    :param css_selector: CSS选择器
    """
    try:
        element = driver.find_element(By.CSS_SELECTOR, css_selector)
        element.click()
    except (TimeoutException, WebDriverException) as e:
        print(f"An error occurred while clicking element: {e}")

def print_api_wrap_fields(driver):
    """
    打印 class="api-wrap" 的全部字段
    :param driver: WebDriver实例
    """
    elements = driver.find_elements(By.CSS_SELECTOR, '.api-wrap')
    for element in elements:
        outer_html = element.get_attribute('outerHTML')
        soup = BeautifulSoup(outer_html, 'html.parser')
        spans = soup.find_all('span')
        if len(spans) >= 2:
            print("key获取成功，即将打印...")
            # 替换 data 字段为 fields
            modified_text = spans[1].text.replace('data', 'fields')
            print(modified_text)

api_key = login_to_backend(driver)
click_element(driver, '#tab-4')
print_api_wrap_fields(driver)
driver.quit()
