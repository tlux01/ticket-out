import itertools
from Get import *


def compute_expected_value_win(track, race_num, bet = 0):
    """
    Retrieve expected value of each horse in certain race
    based on implied probability of win pool

    :param track: race track you want to pull from
    :param race_num: race number
    :param bet: default to $0 bet, added as bet can change pool
                and therefore the expected payout
    :return: none
    """
    win_show_url = get_url(track, race_num)['WPS']

    r_win_show = requests.get(win_show_url)

    data = r_win_show.json()

    pool_totals = data['PoolTotals']
    show_total = 0

    # find total amount of money bet in show pool
    for total in pool_totals:
        if total['PoolType'] == 'SH':
            show_total = int(total['Amount']) + bet
    # entries is dictionary of horses in race
    entries = data['WPSPools']['Entries']
    runners = [] # includes all horses
    active_list = []  # doesn't include scratches
    for horse in entries:
        if horse['Win'] != '-2':  # -2 indicates scratch
            active_list.append(horse["ProgramNumber"])
            runners.append(horse)
        else:
            runners.append("Scratch")

    # turns runners into dictionary with horse as key,
    # horse is type string
    runners = change_dictionary(runners)
    print(runners)
    # all possible top 3 finishers permutations
    perm = perm_list(active_list)
    perm = list(perm)
    for i in runners.keys():
        ex = compute_expected_payout(i, runners, show_total, perm, "WinPct", bet)
        runners[i]["Expected Value"] = ex

    for horse in runners.keys():
        print("Win Horse", horse + ':', runners[horse]["Expected Value"])

    return runners

def compute_expected_value_dd(track, race_num, bet = 0):
    """
    Retrieve expected value of each horse in certain race
    based on implied probability of win pool

    :param track: race track you want to pull from
    :param race_num: race number
    :return: none
    """
    win_show_url = get_url(track, race_num)['WPS']

    r_win_show = requests.get(win_show_url)

    data = r_win_show.json()

    pool_totals = data['PoolTotals']
    show_total = 0

    # find total amount of money bet in show pool
    for total in pool_totals:
        if total['PoolType'] == 'SH':
            show_total = int(total['Amount'])
    # entries is dictionary of horses in race
    entries = data['WPSPools']['Entries']
    runners = []  # includes all horses
    active_list = []  # doesn't include scratches
    for horse in entries:
        if horse['Win'] != '-2':  # -2 indicates scratch
            active_list.append(horse["ProgramNumber"])
            runners.append(horse)
        else:
            runners.append("Scratch")
    # turns runners into dictionary with horse as key,
    # horse is type string
    runners = change_dictionary(runners)
    # all possible top 3 finishers permutations
    perm = perm_list(active_list)
    perm = list(perm)
    # will pays and double pool for current race are stored in previous race
    will_pays = collect_will_pays(track, race_num - 1)
    pool_totals = collect_exotic_pools(track, race_num - 1)
    double_total = int(pool_totals['Double'])
    # get double implied win probabilities
    will_pays = dd_implied(double_total, will_pays)
    for horse in will_pays.keys():
        if will_pays[horse]["Will Pay"] != 'Scratch':
            # multiply by 100 as DD Implied is in decimal form
            runners[horse]["DD Implied"] = will_pays[horse]["DD Implied"] * 100
    for horse in runners.keys():
        ex = compute_expected_payout(horse, runners, show_total, perm, "DD Implied", bet)
        runners[horse]["Expected Value"] = ex

    for horse in runners.keys():
        print("DD Horse", horse + ':', runners[horse]["Expected Value"])
    return runners

def perm_list(active_list):
    """

    :param active_list: list of horses
    :return: list of permutations of size 3 of active_list
    """
    perm = itertools.permutations(active_list, 3)
    return perm

def compute_probabaility(seq, runners, key):
    """
    Uses Harville's Equation to compute probability of
    top three finishing in order of seq

    :param seq: order of to three horses
    :param runners: dictionary of horses
    :return: probability of sequence
    """
    p_1 = float(runners[seq[0]][key]) / 100  # convert to decimal
    p_2 = float(runners[seq[1]][key]) / 100
    p_3 = float(runners[seq[2]][key]) / 100
    prob = (p_1*p_2*p_3) / ((1 - p_1)*(1 - p_1 - p_2))

    return prob

def compute_payout(seq, runners, show_total, horse, bet):
    """
    Profit is net pool less gross amount bet on all show finishers.
    Finishers split profit evenly three ways then divide by gross
    ammount bet on each show finisher for three unique prices

    :param seq: sequence of first, second, third place finishers
    :param runners: dictionary of horses
    :param show_total:
    :param horse: horse you want to compute show payout
    :return: show payout of specified horse
    """

    horse_index = seq.index(horse) # index of wanted horse
    a_horse = int(runners[seq[horse_index]]['Show']) + bet

    # remove horse so we always get the other two horse as
    # index 0 and 1
    seq.remove(horse)
    a_2 = int(runners[seq[0]]['Show'])
    a_3 = int(runners[seq[1]]['Show'])

    # 16% cut is taken from pool
    profit = (show_total *.84 - a_horse - a_2 - a_3) / 3
    payout = 1 + (profit/a_horse)
    return payout

def compute_expected_payout(horse, runners, show_total, perm, key, bet):
    """
    Computes expected payout of horse

    :param horse: horse your computing expected payout for
    :param runners: dictionary of horses
    :param show_total:
    :param perm: all possible 3 horse permutations
    :return: expected payout
    """
    expected_value = 0
    prob_total = 0
    for i in range(len(perm)):
        seq = list(perm[i])
        if horse in seq:
            prob = compute_probabaility(seq, runners, key)
            prob_total += prob
            payout = compute_payout(seq, runners, show_total, horse, bet)
            expected_value += prob*payout
    return expected_value

def dd_implied(double_total, will_pays):
    """
    computes the implied win probability based on the double pool
    and will pays and adds it back into the will pays dictionary
    :param double_total: double pool total
    :param will_pays: dictionary of will pay data for each horse
    :return: will pay dictionary
    """
    total = 0
    for horse in will_pays.keys():
        if will_pays[horse]['Will Pay'] != 'Scratch':
            will_pays[horse]['Num Tickets'] = double_total / will_pays[horse]['Will Pay']
            total += will_pays[horse]['Num Tickets']
    for horse in will_pays.keys():
        if will_pays[horse]['Will Pay'] != 'Scratch':
            will_pays[horse]['DD Implied'] = will_pays[horse]['Num Tickets'] / total

    return will_pays

