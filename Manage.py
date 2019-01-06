from Calculations import *
from WebDriver import *
import time

bet = 2
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

def monitor():
    driver = open_NYRA()
    NYRA_login(driver, 'login.txt')
    active_tracks = find_active_tracks()
    bet_list = {}
    open_tracks = {}
    loop_num = 9
    for track in active_tracks.keys():
        bet_list[track] = {}
        n = find_num_races(track)
        for i in range(2, n + 1):
            bet_list[track][i] = {}
    while True:
        loop_num += 1
        if loop_num == 10:
            loop_num = 0
            open_tracks_keys = list(open_tracks.keys())
            active_tracks_keys = list(active_tracks.keys())
            for track in active_tracks_keys:
                if track in open_tracks_keys:
                    print(track, open_tracks[track])
                    if open_tracks[track] is None:
                        active_tracks.pop(track)
                        open_tracks.pop(track)
                    else:
                        open_tracks[track] = find_if_track_open(track, open_tracks[track]['Error'],
                                                                open_tracks[track])
                else:
                    open_tracks[track] = find_if_track_open(track)
        active_queue = {}
        open_tracks_keys = list(open_tracks.keys())
        for track in open_tracks_keys:
            if open_tracks[track] is None:
                if track in active_queue.keys():
                    active_queue.pop(track)
            elif open_tracks[track]['MTP'] in ['Off', 'Closed']:
                if track in active_queue.keys():
                    current_race = active_queue[track]['Current Race']
                    active_queue.pop(track)
                    file_name = 'betlog.txt'
                    file_name = os.path.join(os.getcwd(), file_name)
                    betlog(bet_list[track][current_race], track,
                           current_race, file_name)
            else:
                if open_tracks[track]['MTP'] < 1 and open_tracks[track]['Current Race'] > 1:
                    active_queue[track] = open_tracks[track]
        active_queue_keys = list(active_queue.keys())
        for track in active_queue_keys:
            if track in open_tracks_keys:
                if open_tracks[track] == None:
                    active_tracks.pop(track)
                    open_tracks.pop(track)
                else:
                    open_tracks[track] = find_if_track_open(track, open_tracks[track]['Error'],
                                                            open_tracks[track])
            else:
                open_tracks[track] = find_if_track_open(track)
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
            current_race = active_queue[track]['Current Race']
            print(current_race, bet_list[track][current_race])

        # checks if active queue is empty
        if not active_queue:
            min_mtp = min_MTP(open_tracks)
            if min_mtp == None:
                print("No more tracks today")
                driver.close()
                break
            else:
                print(min_mtp, "minutes until next bettable race")
                time.sleep(min_mtp * 5)
        else:
            time.sleep(3)



def find_active_tracks():
    active_tracks = {}
    for track in track_list.keys():
        if find_num_races(track) > 0:
            active_tracks[track] = None

    return active_tracks

def min_MTP(open_tracks):
    # use 100 to signify None as no MTP can be greater than 99
    min_mtp = 100
    for track in open_tracks:
        if open_tracks[track] == None:
            pass
        elif open_tracks[track]['Current Race'] == 1:
            min_mtp = min(50, min_mtp)
        elif open_tracks[track]['Error']:
            min_mtp = min(50, min_mtp)
        elif open_tracks[track]['MTP'] in ['Off', 'Closed']:
            min_mtp = min(50, min_mtp)
        else:
            min_mtp = min(open_tracks[track]['MTP'], min_mtp)

    if min_mtp == 100:
        min_mtp = None
    return min_mtp

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

