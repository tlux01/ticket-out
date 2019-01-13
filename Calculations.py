import itertools
from Get import *


def comp_evs_show(track, race_num, bet = 0, bet_list = {}):
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

    r_win_show = requests.get(win_show_url, headers=headers)

    data = r_win_show.json()

    pool_totals = data['PoolTotals']
    show_total = 0

    # find total amount of money bet in show pool
    for total in pool_totals:
        if total['PoolType'] == 'SH':
            show_total = int(total['Amount']) + bet
    print(show_total)
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
    perm = perm_list(active_list, 3)
    perm = list(perm)
    for horse in runners.keys():
        # checks if we have already made a bet on this horse, if we did don't want to compute ev with additional bet factored in
        if horse in bet_list.keys():
            ex = compute_expected_show_payout(horse, runners, show_total, perm, "WinPct", 0)
        else:
            ex = compute_expected_show_payout(horse, runners, show_total, perm, "WinPct", bet)
        runners[horse]["Show Win EV"] = ex

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
        if horse in bet_list.keys():
            ex = compute_expected_show_payout(horse, runners, show_total, perm, "DD Implied", 0)
        else:
            ex = compute_expected_show_payout(horse, runners, show_total, perm, "DD Implied", bet)
        runners[horse]["Show DD EV"] = ex
    return runners

def comp_evs_place(track, race_num, bet = 0):
    win_show_url = get_url(track, race_num)['WPS']

    r_win_show = requests.get(win_show_url, headers = headers)

    data = r_win_show.json()

    pool_totals = data['PoolTotals']
    place_total = 0

    # find total amount of money bet in show pool
    for total in pool_totals:
        if total['PoolType'] == 'PL':
            place_total = int(total['Amount']) + bet
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
    perm = perm_list(active_list, 2)
    perm = list(perm)
    for horse in runners.keys():
        ex = compute_expected_place_payout(horse, runners, place_total, perm, "WinPct", bet)
        runners[horse]["Place Win EV"] = ex

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
        ex = compute_expected_place_payout(horse, runners, place_total, perm, "DD Implied", bet)
        runners[horse]["Place DD EV"] = ex

    return runners
def perm_list(active_list, num):
    """

    :param active_list: list of horses
    :param num: length of sequence
    :return: list of permutations of size num of active_list
    """
    perm = itertools.permutations(active_list, num)
    return perm

def compute_show_prob(seq, runners, key):
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

def compute_place_prob(seq, runners, key):
    p_1 = float(runners[seq[0]][key]) / 100  # convert to decimal
    p_2 = float(runners[seq[1]][key]) / 100
    prob = (p_1 * p_2) / (1 - p_1)

    return prob

def compute_show_payout(seq, runners, show_total, horse, bet):
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
    payout = max(payout, 1.05)
    return payout

def compute_place_payout(seq, runners, place_total, horse, bet):

    horse_index = seq.index(horse)  # index of wanted horse
    a_horse = int(runners[seq[horse_index]]['Place']) + bet

    # remove horse so we always get the other horse as
    # index 0
    seq.remove(horse)
    a_2 = int(runners[seq[0]]['Place'])

    # 16% cut is taken from pool
    profit = (place_total * .84 - a_horse - a_2) / 2
    payout = 1 + (profit / a_horse)
    return payout

def compute_expected_show_payout(horse, runners, show_total, perm, key, bet):
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
            prob = compute_show_prob(seq, runners, key)
            prob_total += prob
            payout = compute_show_payout(seq, runners, show_total, horse, bet)
            expected_value += prob*payout
    return expected_value

def compute_expected_place_payout(horse, runners, show_total, perm, key, bet):
    expected_value = 0
    prob_total = 0
    for i in range(len(perm)):
        seq = list(perm[i])
        if horse in seq:
            prob = compute_place_prob(seq, runners, key)
            prob_total += prob
            payout = compute_place_payout(seq, runners, show_total, horse, bet)
            expected_value += prob * payout
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

def bet_or_cancel(horse_evs, threshold = 1.1):
    """
    returns if we should bet out not, if the average of Show Win EV
    and Show DD EV is above the threshold we output True, otherwise
    outputs False, meaning we cancel bet
    :param horse_evs:
    :param threshold:
    :return:
    """
    win = horse_evs["Show Win EV"]
    dd = horse_evs["Show DD EV"]
    print((win + dd) / 2)
    if win > 1.1 and dd > 1.1:
        return True

    return False