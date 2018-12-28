from selenium import webdriver
import time
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

def login_info(file_name):
    """
    retrieves login credentials and returns them in dictionary
    :param file_name:
    :return:
    """
    with open(file_name) as f:
        usrName = f.readline().strip("\n")
        pssWrd = f.readline().strip("\n")
    f.close()
    return {'username': usrName, 'password': pssWrd}

def place_bet(track_name, bet_amount, program_number):
    """
    places bet on track on horse correspoding to program number,
    uses selenium so it requires a chrome driver
    :param track_name:
    :param bet_amount:
    :param program_number:
    :return:
    """



    credentials = login_info('login.txt')

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.nyrabets.com/#wagering")
    driver.switch_to.frame("gepIframe")

    driver.find_element_by_link_text(track_name).click()
    driver.switch_to.default_content()
    driver.switch_to.frame("loginFrame")
    driver.find_element_by_name('username').send_keys(credentials['username'])
    driver.find_element_by_name('password').send_keys(credentials['password'])
    driver.find_element_by_id('gep-login').click()
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
    for button in buttons:
        print(button.get_attribute("innerText").strip("\n"))
        if button.get_attribute("innerText").strip("\n") == 'Confirm':
            button.click()
    time.sleep(5)
    driver.close()
