from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import os
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

def open_NYRA():
    """
    opens chrome webdriver and goes to NYRA bets
    :return:
    """
    # store chromedriver in same directory as python files
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")

    driver = webdriver.Chrome(executable_path=DRIVER_BIN)
    driver.maximize_window()
    driver.get("https://www.nyrabets.com/#wagering")
    return driver

def NYRA_login(driver, file_name):
    """
    Logs into NYRA site based on info in file name
    :param driver: current webdriver instance
    :param file_name: name of file with login details
    :return:
    """
    driver.switch_to.default_content()
    driver.switch_to.frame("loginFrame")
    with open(file_name) as f:
        usr_name = f.readline().strip("\n") # removes new line character
        pss_wrd = f.readline().strip("\n")
    f.close()
    driver.find_element_by_name('username').send_keys(usr_name)
    driver.find_element_by_name('password').send_keys(pss_wrd)
    driver.find_element_by_id('gep-login').click()


def go_to_track(driver, track):
    """
    goes to specified track after we
    :param driver:
    :param track:
    :return:
    """
    driver.switch_to.default_content()
    driver.switch_to.frame("gepIframe")
    # tries to click on name of track if it can' that is because
    # today's racing dropdown is not open
    try:
        driver.find_element_by_link_text(track).click()  # go to track link
    except:
        # click today's racing dropdown
        driver.find_element_by_id("ui-accordion-leftNavAccordian-header-3").click()
        driver.find_element_by_link_text(track).click()  # go to track link

def go_to_race(driver, race_num, track):
    """
    goes to race webpage at specific track on NYRA, operates by first trying
    to go to the track link which then opens the dropdown for the
    :param driver:
    :param race_num:
    :param track:
    :return:
    """
    try:
        go_to_track(driver, track)
    except:
        pass
    driver.switch_to.default_content()
    driver.switch_to.frame("gepIframe")
    driver.find_element_by_partial_link_text("Race " + str(race_num)).click()

def place_bet(driver, bet_amount, program_number, bet_list):
    """
    places bet on track on horse corresponding to program number,
    uses selenium so it requires a chrome driver
    :param driver:
    :param track_name:
    :param bet_amount:
    :param program_number:
    :return:
    """

    driver.switch_to.default_content()
    driver.switch_to.frame("gepIframe")

    try:
        text = driver.find_element_by_id('gep-programmessage').get_attribute("innerText")
        if "closed" in text:
            print("Betting has closed")
            return bet_list
    except:
        pass
    try:
        driver.find_element_by_xpath("//select[@class='gep-pools']/option[text()='SHW']").click()
    except NoSuchElementException:
        print("No show bets at this race")
        return bet_list

    # clicks on checkbox of certain horse we want to bet on
    program = "//input[@programnumber = '" + str(program_number) + "']"

    # avoids stale error based on improper DOM load
    attempts = 0
    while attempts < 5:
        time.sleep(.5)
        attempts += 1
        try:
            driver.find_element_by_xpath(program).click()
            break
        except Exception as e:
            print(e)
    if attempts == 5:
        print("Could not place bet on", program_number)
        return bet_list

    while attempts < 5:
        time.sleep(.5)
        attempts += 1
        try:
            # second expand all is what we want
            driver.find_element_by_xpath("//input[@class='gep-inputcontrol-stake']").clear()
            break
        except Exception as e:
            print(e)

    driver.find_element_by_xpath("//input[@class='gep-inputcontrol-stake']").send_keys(str(bet_amount))
    try:
        # checks if program message is shown saying betting has closed
        text = driver.find_element_by_id('gep-programmessage').get_attribute("innerText")
        if "closed" in text:
            print("Betting has closed")
            return bet_list
    except:
        pass

    try:
        text = driver.find_element_by_xpath("//div[@class='gep-message gep-bet-error']").get_attribute("innerText")
        if "not open" in text:
            driver.find_element_by_xpath("//button[@class='gep-cancelAll gep-button']").click()
            print("Betting has just closed")
            return bet_list
    except:
        pass

    driver.find_element_by_xpath("//button[@class='gep-placeSelected gep-button gep-default']").click()
    div = driver.find_elements_by_xpath("//div[@class='ui-dialog-buttonset']")
    buttons = div[1].find_elements_by_tag_name("button")

    for button in buttons:
        if button.get_attribute("innerText").strip("\n") == 'Confirm':
            button.click()
    time.sleep(1)
    receipt = driver.find_element_by_xpath("//div[@class='gep-receiptLine']")
    id = receipt.find_element_by_class_name("gep-value").get_attribute("innerHTML")
    # error checking for not recieving the right ticket id #
    if len(id) == 1:
        print("Could not place bet on", program_number)
        return bet_list

    bet_list[program_number] = id
    print("--------------------------")
    print("Bet on horse", program_number)
    print("--------------------------")
    return bet_list
    # time.sleep(9)
    # driver.close()

def cancel_bet(driver, bet_list, horse):
    bet_id = bet_list[horse]
    # reloads content
    driver.switch_to.default_content()
    driver.switch_to.frame("gepIframe")
    try:
        text = driver.find_element_by_id('gep-programmessage').get_attribute("innerText")
        if "closed" in text:
            print("Betting has closed")
            return bet_list
    except:
        pass
    #to make sure bets load, three clicks to refresh page
    driver.find_element_by_xpath("//a[@href='#gep-betHistory']").click()
    driver.find_element_by_xpath("//a[@href='#gep-betSlip']").click()
    driver.find_element_by_xpath("//a[@href='#gep-betHistory']").click()
    time.sleep(1)
    driver.find_element_by_xpath("//select[@class='gep-trackracefilter']"
                                 "/option[text()='This Race']").click()

    attempts = 0
    while attempts < 10:
        time.sleep(.5)
        attempts += 1
        try:
            # second expand all is what we want
            driver.find_elements_by_xpath("//a[@class='gep-expandAll']")[1].click()
            break
        except Exception as e:
            print(e)

    my_bets = driver.find_element_by_class_name("gep-list")
    my_bets = my_bets.find_elements_by_xpath("//div[@class='gep-bet gep-status-none  gep-betCategory5']")
    # list is the list of bets (either canceled or active) that is seen in the my bets dropdown
    for item in my_bets:
        info = item.find_element_by_class_name("gep-extraInfo")
        info = info.find_elements_by_class_name("gep-receiptLine")
        button = item.find_element_by_class_name("gep-betSelectorBox")
        for line in info:
            ticket_line = line.find_element_by_class_name("gep-attrib").get_attribute("innerHTML")
            if ticket_line == "Ticket #:":
                ticket_num = line.find_element_by_class_name("gep-value").get_attribute("innerHTML")
                if ticket_num == bet_id:
                    button.click()

    #cancel bet
    driver.find_element_by_xpath("//button[@class='gep-cancel gep-button gep-default']").click()
    ui_buttons = driver.find_elements_by_xpath("//button[@class='ui-button ui-widget ui-state-default"
                                               " ui-corner-all ui-button-text-only']")
    for ui_button in ui_buttons:
        if ui_button.get_attribute("innerText").strip("\n") == 'Confirm':
            ui_button.click()
    time.sleep(1)

    try:
        # gep-error will show if we cannot get bet up in time
        driver.find_element_by_xpath("//span[@class='gep-error']")
        print("Could not cancel bet on", bet_id)
    except:
        bet_list.pop(horse)
        print("--------------------------")
        print("Canceled bet on horse", horse)
        print("--------------------------")

    #click close
    attempts = 0
    while attempts < 10:
        time.sleep(.5)
        attempts += 1
        try:
            # second expand all is what we want
            driver.find_element_by_xpath("//button[@class='gep-close gep-button gep-default']").click()
            break
        except Exception as e:
            print(e)
    return bet_list

def track_open(driver):
    """
    once on correct page, returns the MTP of the track,
    can be OFF or FIN as well
    :return:
    """
    header = driver.find_element_by_class_name("gep-raceDetails")
    span = header.find_elements_by_tag_name("span")
    innerHTML = span[0].get_attribute("innerHTML")
    info = innerHTML.split() # because inner HTML can be of form "22 MTP"
    MTP = info[0]
    if MTP == 'OFF':
        return MTP
    elif MTP == 'FIN':
        return MTP
    else:
        return int(MTP)


# add place bet error when we try to place bet but the track closes just as we do so