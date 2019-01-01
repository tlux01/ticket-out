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
    race_stat = collect_race_status(track, current_race)
    if race_stat["raceStatus"] == "Open":
        print("Race", current_race, "at", track)
        MinToPost = int(track_stat["Mtp"])
        if current_race == 1:
            print("No bets on first race")
        else:
            while(MinToPost > 19):
                race_stat = collect_race_status(track, current_race)
                MinToPost = int(race_stat["mtp"])
                print("MTP:", MinToPost)
                time.sleep(30 * MinToPost)
            while race_stat["raceStatus"] == 'Open':
                go_to_race(driver, current_race, track_list[track]["NYRA"])
                track_stat = track_info(track)
                current_race = track_stat["RaceNum"]
                show_ev = comp_evs_show(track, current_race)
                for horse in show_ev.keys():
                    print(horse, end=" ")
                    if bet_or_cancel(show_ev[horse]):
                        if horse not in bet_list.keys():
                            id = place_bet(driver, 1, horse)
                            bet_list[horse] = id
                            print("--------------------------")
                            print("Bet on horse", horse)
                            print("--------------------------")
                    else:
                        if horse in bet_list.keys():
                            go_to_race(driver, current_race, track)
                            cancel_bet(driver, bet_list[horse])
                            bet_list.pop(horse)
                            print("--------------------------")
                            print("Canceled bet on horse", horse)
                            print("--------------------------")

                race_stat = collect_race_status(track, current_race)
                print(bet_list)
                time.sleep(10)


            #prints final expected values after close
            show_ev = comp_evs_show(track, current_race)
            for horse in show_ev.keys():
                avg = (show_ev[horse]["Show Win EV"] * .5) + \
                      (show_ev[horse]["Show DD EV"] * .5)
                print(horse + ":", str(avg))

    print("Race", current_race, "is", race_stat["raceStatus"])
    driver.close()


def monitor_wrapper(track):
    try:
        monitor(track)
    except Exception as e:
        print(e)