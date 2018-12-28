import csv
import os
import time
from Calculations import *


def track_data_collector(track, start_from = 1):
    """
    actively runs until all data from the track is collected for the day
    :param track:
    :param start_from: race you start looking from, default is 1
    :return:
    """

    filename = track + " Races.csv"
    print(filename)
    # writes new file if file not in our Data folder
    if not os.path.isfile('C:/Users/tylux/Desktop/Projects/Track/Data/' + filename):
        write_header(track)
    # want to wait until thirty minutes after the post time so results
    # can get in
    num_races = find_num_races(track)
    if num_races == 0:
        print(track, "had no races today")
    else:
        race = track_start(track)
        first_post_time = race['FirstPostTime']
        status = race['Status']
        collect = False
        while not collect:
            now = datetime.now()
            if now > first_post_time and status == 'Closed':
                for i in range(1, num_races + 1):
                    try:
                        write_to_csv(track, i)
                    except Exception as e:
                        print("Race", i, "had error", e)
                collect = True
            else:
                print(track, " has not closed yet")
                # if too early waits 5 minutes before checking again
                time.sleep(300)








def write_to_csv(track, race_num):
    """
    appends track data onto csv
    :param track:
    :param race_num:
    :return:
    """

    first_race = False
    num_races = find_num_races(track)
    WPS = collect_WPS(track, race_num)
    results = collect_results(track, race_num)
    # checks if race is the first race as error will occur
    # as no will pays in the first race
    if race_num != 1:
        will_pays = collect_will_pays(track, race_num - 1)
        pool_totals = collect_exotic_pools(track, race_num - 1)
        double_total = int(pool_totals['Double'])
        will_pays = dd_implied(double_total, will_pays)
    else:
        first_race = True


    expected_values_dd = compute_expected_value_dd(track, race_num)
    expected_values_win = compute_expected_value_win(track, race_num)

    # below is the building of the 2-d list that will represent the rows
    # and columns in our csv
    content = []
    for horse_num in WPS.keys():
        figs = WPS[horse_num]
        row = []
        date = str(track_start(track)['FirstPostTime'].date())
        row.append(date), row.append(track)
        row.append(race_num), row.append(horse_num)
        if figs != 'Scratch':
            row.append(figs['Win']), row.append(figs['Place'])
            row.append(figs['Show']), row.append(figs['WinPct'])
            row.append(figs['PlacePct']), row.append(figs['ShowPct'])
        else:
            for i in range(6):
                row.append(0)
        if not first_race:
            willp = will_pays[horse_num]
            if willp['Will Pay'] != 'Scratch':
                row.append(willp['Will Pay'])
                row.append(willp['DD Implied'])
            else:
                row.append(0)
                row.append(0)
        else:
            row.append(0)
            row.append(0)
        if horse_num in results.keys():
            result = results[horse_num]['Result']
            row.append(result)
            if result == 1:
                row.append(results[horse_num]['Win Payout'])
                row.append(results[horse_num]['Place Payout'])
                row.append(results[horse_num]['Show Payout'])
            elif result == 2:
                row.append(0)
                row.append(results[horse_num]['Place Payout'])
                row.append(results[horse_num]['Show Payout'])
            else:
                row.append(0)
                row.append(0)
                row.append(results[horse_num]['Show Payout'])
        else:
            for i in range(4):
                row.append(0)
        if horse_num in expected_values_dd.keys():
            row.append(expected_values_dd[horse_num]["Expected Value"])
        else:
            row.append(0)
        if horse_num in expected_values_win.keys():
            row.append(expected_values_win[horse_num]["Expected Value"])
        else:
            row.append(0)
        content.append(row)



    file_name = 'C:/Users/tylux/Desktop/Projects/Track/Data/'+ track + ' Races.csv'
    with open(file_name, 'a', newline='') as f:
        writer = csv.writer(f)
        for i in range(len(content)):
            writer.writerow(content[i])


def write_header(track):
    """
    creates a new csv and writes the header into it
    :param track:
    :return:
    """
    header = ['Date', 'Track', 'Race', 'Horse',
              'Win Pool ($)', 'Place Pool ($)', 'Show Pool ($)',
              'Win Pct', 'Place Pct ($)', 'Show Pct ($)', 'Will Pay', 'DD Implied',
              'Result', 'Win Payout', 'Place Payout', 'Show Payout',
              'DD EV', 'Win EV']
    file_name = 'C:/Users/tylux/Desktop/Projects/Track/Data/' + track + ' Races.csv'
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)



