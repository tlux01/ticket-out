from Calculations import *
from WebDriver import *
import time

bet = 2
def monitor(driver, track, bet_list):

    driver.implicitly_wait(3)
    NYRA_login(driver, "login.txt")
    go_to_track(driver, track_list[track]["NYRA"])
    track_stat = track_info(track)
    current_race = int(track_stat["RaceNum"])
    print(track_stat)
    race_stat = track_open(driver)
    print(race_stat)
    if race_stat != "OFF" and race_stat != "FIN":
        print("Race", current_race, "at", track)
        if current_race == 1:
            print("No bets on first race")
        else:
            while(race_stat > 0):
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

    with open(file_name, 'a') as f:
        date = datetime.now()
        f.write(str(date) + ' ' + track + ' ' + str(current_race) + '\n')
        if bet_list:
            for horse in bet_list.keys():
                f.write('Horse: ' + horse + ' Amount: ' + str(bet) +
                        ' Ticket #: ' + str(bet_list[horse]) + '\n')
        else:
            f.write("No Bets\n")

    answer = None
    while answer not in ("y", "n"):
        answer = input("Do you want to close? [y/n]: ")
        if answer == "y":
            driver.close()
            return None
        elif answer == "n":
            print(driver)
            return driver
        else:
            print("Please enter yes or no.")


def monitor_wrapper(track):
    bet_list = {}
    driver = open_NYRA()
    try:
        driver = monitor(driver, track, bet_list)
    except Exception as e:
        print(e)
        print(bet_list)
        bets = bet_list.keys()
        for horse in bets:
            cancel_bet(driver, bet_list, horse)
    print(bet_list)
    return driver

def monitor1():

    active_tracks = {}
    for track in track_list.keys():
        if find_num_races(track) > 0:
            track_stat = track_info(track)
            current_race = int(track_stat["RaceNum"])
            race_stat = collect_race_status(track, current_race)
            active_tracks[track] = {'MTP' : race_stat['mtp'],
                                    'Current Race' : current_race}
    while True:
        for track in active_tracks.keys():
            time.sleep(2)
            track_stat = track_info(track)
            current_race = int(track_stat["RaceNum"])
            race_stat = collect_race_status(track, current_race)
            print(race_stat)
            print(track, track_stat['RaceStatus'])
            print(active_tracks[track]['Current Race'],
                  active_tracks[track]['MTP'])

            active_tracks[track] = {'MTP': race_stat['mtp'],
                                    'Current Race': current_race}

