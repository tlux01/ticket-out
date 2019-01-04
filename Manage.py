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
    race_stat = track_open(driver)
    if current_race == 1:
        print("No bets on first race")
        return
    if race_stat != "OFF" and race_stat != "FIN":
        print("Race", current_race, "at", track)
        while (race_stat > 0):
            race_stat = track_open(driver)
            time.sleep(race_stat * 30)
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
    betlog(bet_list, track, current_race, file_name)

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

def betlog(bet_list, track, current_race, file_name):
    with open(file_name, 'a') as f:
        date = datetime.now()
        f.write(str(date) + ' ' + track + ' ' + str(current_race) + '\n')
        if bet_list:
            for horse in bet_list.keys():
                f.write('Horse: ' + horse + ' Amount: ' + str(bet) +
                        ' Ticket #: ' + str(bet_list[horse]) + '\n')
        else:
            f.write("No Bets\n")

def monitor1():
    driver = open_NYRA()
    NYRA_login(driver, 'login.txt')
    active_tracks = find_active_tracks()
    bet_list = {}
    open_tracks = {}
    for track in active_tracks:
        bet_list[track] = {}
        n = find_num_races(track)
        for i in range(2, n + 1):
            bet_list[track][i] = {}
    while True:
        open_tracks_keys = list(open_tracks.keys())
        for track in active_tracks:
            if track in open_tracks_keys:
                if open_tracks[track] == None:
                    pass
                else:
                    open_tracks[track] = find_if_track_open(track, open_tracks[track]['Error'],
                                                            open_tracks[track])
            else:
                open_tracks[track] = find_if_track_open(track)
        active_queue = {}
        for track in open_tracks_keys:
            print(track, open_tracks[track])
            if open_tracks[track] == None:
                if track in active_queue.keys():
                    active_queue.pop(track)
            elif open_tracks[track]['MTP'] in ['Off', 'Closed']:
                if track in active_queue.keys():
                    active_queue.pop(track)
            else:
                if open_tracks[track]['MTP'] < 1 and open_tracks[track]['Current Race'] > 1:
                    active_queue[track] = open_tracks[track]
        active_queue_keys = list(active_queue.keys())
        for track in active_queue_keys:
            if active_queue[track]['Error']:
                active_queue.pop(track)
                pass
            else:
                current_race = active_queue[track]['Current Race']
                try:
                    show_ev = comp_evs_show(track, current_race, bet)
                except Exception as e:
                    print(type(e).__name__)
                    print(e)
                    open_tracks[track]['Error'] = True
                    go_to_race(driver, current_race, track_list[track]["NYRA"])
                    bets = list(bet_list[track][current_race].keys())
                    track_bet_list = bet_list[track][current_race]
                    for horse in bets:
                        track_bet_list = cancel_bet(driver, track_bet_list, horse)
                    bet_list[track][current_race] = track_bet_list
                    break
                for horse in show_ev.keys():
                    print(horse, end=" ")
                    if bet_or_cancel(show_ev[horse]):
                        if horse not in bet_list[track][current_race].keys():
                            print(current_race, track_list[track]["NYRA"])
                            go_to_race(driver, current_race, track_list[track]["NYRA"])
                            track_bet_list = bet_list[track][current_race]
                            time.sleep(1)
                            track_bet_list = place_bet(driver, bet, horse, track_bet_list)
                            bet_list[track][current_race] = track_bet_list
                    else:
                        if horse in bet_list[track][current_race].keys():
                            print(current_race, track_list[track]["NYRA"])
                            go_to_race(driver, current_race, track_list[track]["NYRA"])
                            track_bet_list = bet_list[track][current_race]
                            time.sleep(1)
                            track_bet_list = cancel_bet(driver, track_bet_list, horse)
                            bet_list[track][current_race] = track_bet_list
        print(active_queue)
        for track in active_queue:
            print(track)
            for race in bet_list[track].keys():
                print(race, bet_list[track][race])

        time.sleep(5)



def find_active_tracks():
    active_tracks = []
    for track in track_list.keys():
        if find_num_races(track) > 0:
            active_tracks.append(track)

    return active_tracks

def find_if_track_open(track, error = False, previous_open = None):
    open_track = None
    track_stat = track_info(track)
    if error:
        current_race = int(track_stat["RaceNum"])
        if previous_open['Current Race'] == current_race:
            return previous_open
        else:
            if track_stat['Status'] == 'Open':
                current_race = int(track_stat["RaceNum"])
                race_stat = collect_race_status(track, current_race)
                if track_stat['RaceStatus'] == 'Off':
                    open_track = {'MTP': 'Off', 'Current Race': current_race,
                                  'Error': False}
                elif track_stat['RaceStatus'] == 'Closed':
                    open_track = {'MTP': 'Off', 'Current Race': current_race,
                                  'Error': False}
                else:
                    open_track = {'MTP': race_stat['mtp'],
                                  'Current Race': current_race,
                                  'Error': False}
    else:
        if track_stat['Status'] == 'Open':
            current_race = int(track_stat["RaceNum"])
            race_stat = collect_race_status(track, current_race)
            if track_stat['RaceStatus'] == 'Off':
                open_track = {'MTP': 'Off', 'Current Race': current_race,
                                     'Error': False}
            elif track_stat['RaceStatus'] == 'Closed':
                open_track = {'MTP': 'Off', 'Current Race': current_race,
                                     'Error': False}
            else:
                open_track = {'MTP': race_stat['mtp'],
                                      'Current Race': current_race,
                                      'Error': False}

    return open_track

