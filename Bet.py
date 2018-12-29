from selenium import webdriver
import time
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

def open_NYRA():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.nyrabets.com/#wagering")
    return driver

def NYRA_login(file_name, driver):

    with open(file_name) as f:
        usrName = f.readline().strip("\n")
        pssWrd = f.readline().strip("\n")
    f.close()
    driver.find_element_by_name('username').send_keys(usrName)
    driver.find_element_by_name('password').send_keys(pssWrd)
    driver.find_element_by_id('gep-login').click()
    return driver

def place_bet(driver, track_name, bet_amount, program_number):
    """
    places bet on track on horse correspoding to program number,
    uses selenium so it requires a chrome driver
    :param driver:
    :param track_name:
    :param bet_amount:
    :param program_number:
    :return:
    """

    driver.switch_to.frame("gepIframe")
    driver.find_element_by_link_text(track_name).click()
    driver.switch_to.default_content()
    driver.switch_to.frame("loginFrame")
    driver = NYRA_login('login.txt', driver)
    driver.switch_to.default_content()
    driver.switch_to.frame("gepIframe")

    driver.find_element_by_xpath("//select[@class='gep-pools']/option[text()='PLC']").click()
    program = "//input[@programnumber = '" + str(program_number) + "']"
    # avoids stale error based on fast DOM load
    attempts = 0
    while attempts < 100:
        attempts += 1
        try:
            driver.find_element_by_xpath(program).click()
            break
        except Exception as e:
            print(e)

    driver.find_element_by_xpath("//input[@class='gep-inputcontrol-stake']").clear()
    driver.find_element_by_xpath("//input[@class='gep-inputcontrol-stake']").send_keys(str(bet_amount))
    driver.find_element_by_xpath("//button[@class='gep-placeSelected gep-button gep-default']").click()
    div = driver.find_elements_by_xpath("//div[@class='ui-dialog-buttonset']")
    buttons = div[1].find_elements_by_tag_name("button")
    time.sleep(2)
    for button in buttons:
        print(button.get_attribute("innerText").strip("\n"))
        if button.get_attribute("innerText").strip("\n") == 'Confirm':
            button.click()
    # time.sleep(9)
    # driver.close()
    return driver