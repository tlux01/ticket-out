from Get import *
from Calculations import *
import time
from datetime import datetime
def monitor(track):


    track_stat = track_info(track)
    current_race = int(track_stat["RaceNum"])
    race_stat = collect_race_status(track, current_race)
    MinToPost = int(track_stat["Mtp"])

    while(MinToPost > 100):
        time.sleep(60)
        race_stat = collect_race_status(track, current_race)
        MinToPost = int(track_stat["Mtp"])
    while track_stat['RaceStatus'] == 'Open':
        track_stat = track_info(track)
        current_race = track_stat["RaceNum"]
        MinToPost = track_stat["Mtp"]
        show_ev = comp_evs_show(track, current_race)
        for horse in show_ev.keys():
            avg = (show_ev[horse]["Show Win EV"] *.5) + \
                  (show_ev[horse]["Show DD EV"] *.5)
            if avg > 1:
                print(horse + ":", str(avg))
        print("------------------------")
        time.sleep(10)

    show_ev = comp_evs_show(track, current_race)
    for horse in show_ev.keys():
        avg = (show_ev[horse]["Show Win EV"] * .5) + \
              (show_ev[horse]["Show DD EV"] * .5)
        print(horse + ":", str(avg))