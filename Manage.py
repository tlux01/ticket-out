from Calculations import *
from WebDriver import *
import time

bet = 2
def monitor(track):

    bet_list = {}
    driver = open_NYRA()
    driver.implicitly_wait(10)
    NYRA_login("login.txt", driver)
    go_to_track(driver, track_list[track]["NYRA"])
    track_stat = track_info(track)
    current_race = int(track_stat["RaceNum"])
    race_stat = track_open(driver)
    if race_stat != "OFF" and race_stat != "FIN":
        print("Race", current_race, "at", track)
        if current_race == 1:
            print("No bets on first race")
        else:
            while(race_stat > 10):
                race_stat = track_open(driver)
                time.sleep(race_stat*30)
            while race_stat != "OFF" and race_stat != "FIN":
                print(track_open(driver))
                show_ev = comp_evs_show(track, current_race, bet)
                for horse in show_ev.keys():
                    print(horse, end=" ")
                    if bet_or_cancel(show_ev[horse]):
                        if horse not in bet_list.keys():
                            go_to_race(driver, current_race, track_list[track]["NYRA"])
                            time.sleep(1)
                            bet_list = place_bet(driver, bet, horse, bet_list)
                    else:
                        if horse in bet_list.keys():
                            go_to_race(driver, current_race, track_list[track]["NYRA"])
                            time.sleep(1)
                            bet_list = cancel_bet(driver, bet_list, horse)
                time.sleep(2)
                race_stat = track_open(driver)
                print(bet_list)
    print("Race", current_race, "is", race_stat)
    file_name = 'betlog.txt'
    file_name = os.path.join(os.getcwd(), file_name)

    with open(file_name, 'w') as f:
        date = datetime.now()
        f.write(str(date) + ' ' + track + ' ' + str(current_race) + '\n')
        if bet_list:
            for horse in bet_list.keys():
                f.write('Horse: ' + horse + ' Amount: ' + str(bet) +
                        ' Ticket #: ' + str(bet_list[horse]))
        else:
            f.write("No Bets")

    answer = None
    while answer not in ("y", "n"):
        answer = input("Do you want to close? [y/n]: ")
        if answer == "y":
            driver.close()
            return None
        elif answer == "n":
            return driver
        else:
            print("Please enter yes or no.")



def monitor_wrapper(track):
    try:
        monitor(track)
    except Exception as e:
        print(e)

def monitor1(track):
    pit = 1
