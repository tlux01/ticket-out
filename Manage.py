from Calculations import *
from WebDriver import *
import time


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
                show_ev = comp_evs_show(track, current_race, 2)
                for horse in show_ev.keys():
                    print(horse, end=" ")
                    if bet_or_cancel(show_ev[horse]):
                        if horse not in bet_list.keys():
                            go_to_race(driver, current_race, track_list[track]["NYRA"])
                            time.sleep(1)
                            bet_list = place_bet(driver, 2, horse, bet_list)
                            print("--------------------------")
                            print("Bet on horse", horse)
                            print("--------------------------")
                    else:
                        if horse in bet_list.keys():
                            go_to_race(driver, current_race, track_list[track]["NYRA"])
                            time.sleep(1)
                            cancel_bet(driver, bet_list, horse)
                            print("--------------------------")
                            print("Canceled bet on horse", horse)
                            print("--------------------------")
                time.sleep(2)
                race_stat = track_open(driver)
                print(bet_list)




    print("Race", current_race, "is", race_stat)
    driver.close()


def monitor_wrapper(track):
    try:
        monitor(track)
    except Exception as e:
        print(e)

def monitor1(track):
    pit = 1
