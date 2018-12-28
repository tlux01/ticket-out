from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from pynput.keyboard import Key, Controller
driver = webdriver.Chrome()

with open("login.txt") as f:
    usrName = f.readline()
    pssWrd = f.readline()
f.close()

bet_amount = '10'

driver.maximize_window()
driver.get("https://www.nyrabets.com/#wagering")
driver.switch_to.frame("gepIframe")


driver.find_element_by_link_text("Fair Grounds").click()
driver.switch_to.default_content()
driver.switch_to.frame("loginFrame")
driver.find_element_by_name('username').send_keys(usrName)
driver.find_element_by_name('password').send_keys(pssWrd)
driver.find_element_by_id('gep-login').click()
driver.switch_to.default_content()
driver.switch_to.frame("gepIframe")

driver.find_element_by_xpath("//select[@class='gep-pools']/option[text()='PLC']").click()
time.sleep(1)
# avoids stale error based on fast DOM load
attempts = 0
while attempts < 100:
    attempts += 1
    try:
        driver.find_element_by_xpath("//input[@programnumber = '4']").click()
        break
    except Exception as e:
        print(e)

driver.find_element_by_xpath("//input[@class='gep-inputcontrol-stake']").clear()
driver.find_element_by_xpath("//input[@class='gep-inputcontrol-stake']").send_keys(bet_amount)
driver.find_element_by_xpath("//button[@class='gep-placeSelected gep-button gep-default']").click()
keyboard = Controller()
time.sleep(2)
# TAB TAB ENTER to click confirm bet
keyboard.press(Key.tab)
keyboard.release(Key.tab)
keyboard.press(Key.tab)
keyboard.release(Key.tab)
keyboard.press(Key.enter)
keyboard.release(Key.enter)