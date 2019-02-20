import requests
from datetime import datetime
from ID import get_url, track_list, tracks_to_bet

# to make clean get requests need this header
headers = {
     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}

def change_dictionary(runners):
    """
    Turn json into dictionary where keys are horse
    numbers

    :param runners: unformatted horse list json
    :return: reformatted dictionary
    """
    dict = {}
    for horse in runners:
        if type(horse) != str:
            i = horse.pop('ProgramNumber')
            dict[i] = horse
    return dict


def find_num_races(track):
    """
    collects number of races running at a track today
    :param track:
    :return: number of races
    """
    schedule_url = get_url(track)['Races']
    schedule = requests.get(schedule_url, headers= headers)
    data = schedule.json()
    print(data)
    try:
        num = int(data[-1]['race'])
    except:
        num = 0
    return num

def collect_WPS(track, race_num):
    """
    collect each horse's win place show pools, how much
    was bet on each horse, percentages
    :param track:
    :param race_num:
    :return:
    """
    data_url = get_url(track, race_num)['WPS']
    data = requests.get(data_url, headers= headers)
    WPS = data.json()
    entries = WPS['WPSPools']['Entries']
    totals = {}
    for horse in entries:
        num = horse["ProgramNumber"]
        if horse['Win'] != '-2':
            dict = horse
            dict.pop("ProgramNumber")
            totals[num] = dict
        else:
            totals[num] = "Scratch"
    return totals

def get_all_info():
    """
    returns info of all tracks
    :param track:
    :return: dict
    """
    # track url doesnt change with different track
    track_url = get_url("Aqueduct")['Track']
    tracks = requests.get(track_url, headers= headers)
    data = tracks.json()
    data = data['CurrentRace']
    return data



def get_track_info(track, data):
    for race in data:
        race_copy = {**race}
        if race["BrisCode"] == track_list[track]["BrisCode"]:
            time = race["FirstPostTime"]
            race_copy["FirstPostTime"] = to_datetime(time)
            return race_copy

def to_datetime(time):
    if "-05:00" in time:
        time = time.replace("-05:00", "")
        time = time.replace("T", " ")
        # change string to datetime
        time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        return time
    else:
        print("ERROR in time parsing")
        raise ValueError

def collect_race_status(track, race_num):
    schedule_url = get_url(track)['Races']
    schedule = requests.get(schedule_url, headers= headers)
    data = schedule.json()
    for race in data:
        if int(race['race']) == race_num:
            return race

def collect_results(track, race_num):
    """
    grabs top 3 finishers and their respective win, place,
    and show payouts
    :param track:
    :param race_num:
    :return:
    """
    result_url = get_url(track, race_num)['Results']
    results = requests.get(result_url, headers= headers)
    data = results.json()
    WPS = data['Results']['WPS']['Entries']
    results = {}
    if len(WPS) == 3:
        # first place horse is first in list
        place = 1
        for horse in WPS:
            horse_num = str(horse["ProgramNumber"])
            results[horse_num] = {}
            results[horse_num]['Result'] = place
            for pool in horse["Pools"]:
                # divide by two to turn payout into basis of $1
                if pool['PoolType'] == 'WN':
                    results[horse_num]['Win Payout'] = (float(pool['Value']) / 2)
                if pool['PoolType'] == 'PL':
                    results[horse_num]['Place Payout'] = (float(pool['Value']) / 2)
                if pool['PoolType'] == 'SH':
                    results[horse_num]['Show Payout'] = (float(pool['Value']) / 2)
            # move on to horse in the next place
            place += 1
    return results


def collect_exotic_pools(track, race_num):
    """
    collect double pool of certain race
    :param track:
    :param race_num:
    :return:
    """
    exotic_url = get_url(track, race_num)['Pools']
    exotics = requests.get(exotic_url, headers= headers)
    data = exotics.json()
    pool_totals = {}
    for pool in data['PoolTotals']:
        if pool['PoolType'] == 'EX':
            pool_totals['Exacta'] = pool['Amount']
        if pool['PoolType'] == 'TR':
            pool_totals['Trifecta'] = pool['Amount']
        if pool['PoolType'] == 'QD':
            pool_totals['Superfecta'] = pool['Amount']
        if pool['PoolType'] == 'DD':
            pool_totals['Double'] = pool['Amount']
        if pool['PoolType'] == 'P3':
            pool_totals['Pick 3'] = pool['Amount']
    return pool_totals

def collect_will_pays(track, race_num):
    """
    grabs will pay data from a certain race
    :param track:
    :param race_num:
    :return: dictionary indexed by horse number with will pays information
    """
    will_pay_url = get_url(track, race_num)['Will Pays']
    will_pay = requests.get(will_pay_url, headers= headers)
    data = will_pay.json()
    will_pays = {}
    pools = data['WillPays']['Pools']
    for pool in pools:
        # will pays for double
        if pool['Pooltype'] == 'DD':
            entries = pool['Entries']
            for horse in entries:
                will_pays[horse['ProgramNumber']] = {}
                # if horse doesn't have value produces error, means scratch
                if 'Value' in horse.keys():
                    val = horse['Value']
                    if val == ' SC':
                        will_pays[horse['ProgramNumber']]['Will Pay'] = 'Scratch'
                    elif val == ' NM':
                        will_pays[horse['ProgramNumber']]['Will Pay'] = 'None'
                    else:
                        will_pays[horse['ProgramNumber']]['Will Pay'] = float(horse['Value'])
                else:
                    will_pays[horse['ProgramNumber']]['Will Pay'] = 'Scratch'
    return will_pays

