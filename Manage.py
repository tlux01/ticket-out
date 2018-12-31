from Calculations import *
import time


def monitor(track):


    track_stat = track_info(track)
    current_race = int(track_stat["RaceNum"])
    race_stat = collect_race_status(track, current_race)
    if race_stat["raceStatus"] == "Open":
        print("Race", current_race, "at", track)
        MinToPost = int(track_stat["Mtp"])
        if current_race == 1:
            print("No bets on first race")
        else:
            while(MinToPost > 1):
                race_stat = collect_race_status(track, current_race)
                MinToPost = int(race_stat["mtp"])
                print("MTP:", MinToPost)
                time.sleep(30 * MinToPost)
            while race_stat["raceStatus"] == 'Open':
                track_stat = track_info(track)
                current_race = track_stat["RaceNum"]
                show_ev = comp_evs_show(track, current_race)
                for horse in show_ev.keys():
                    if bet_or_cancel(show_ev[horse]):
                        print("--------------------------")
                        print("Bet on horse", horse)
                        print("--------------------------")
                race_stat = collect_race_status(track, current_race)
                print(race_stat)
                time.sleep(10)

            #prints final expected values after close
            show_ev = comp_evs_show(track, current_race)
            for horse in show_ev.keys():
                avg = (show_ev[horse]["Show Win EV"] * .5) + \
                      (show_ev[horse]["Show DD EV"] * .5)
                print(horse + ":", str(avg))
    else:
        print("Race", current_race, "is", race_stat["raceStatus"])

def monitor_wrapper(track):
    try:
        monitor(track)
    except Exception as e:
        print(e)