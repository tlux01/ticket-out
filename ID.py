# BrisCode, TrackType, and AtabCode are for twinspires url
# NYRA is for name of track on NYRA Bets
track_list = {
              "Aqueduct": {'BrisCode': "aqu", "TrackType": "Thoroughbred", 'AtabCode': 'AQD',
                           'NYRA': 'Aqueduct'},
              # "Churchill Downs": {'BrisCode': "CD", "TrackType": "Thoroughbred", 'AtabCode': None},
              # "Del Mar": {'BrisCode': "DMR", "TrackType": "Thoroughbred", 'AtabCode': None},
              "Fair Grounds": {'BrisCode': 'fg', 'TrackType': 'Thoroughbred', 'AtabCode': 'JGD',
                               'NYRA': 'Fair Grounds'},
              "Golden Gate Fields" : {'BrisCode': "gg", 'TrackType': "Thoroughbred", 'AtabCode': 'GGD',
                                      'NYRA': 'Golden Gate'},
              "Gulfstream Park": {'BrisCode': "gp", "TrackType": "Thoroughbred", 'AtabCode': "GPM",
                                  'NYRA': 'Gulfstream'},
              "Hawthorne": {'BrisCode': "haw", "TrackType": "Thoroughbred", 'AtabCode': "HAD",
                            'NYRA': 'Hawthorne'},
              "Laurel Park": {'BrisCode': "lrl", 'TrackType': "Thoroughbred", 'AtabCode': 'LRM',
                              'NYRA': 'Laurel'},
              "Los Alamitos QH" : {'BrisCode': "la", 'TrackType': "Thoroughbred", 'AtabCode': 'LQN'},
              "Penn National" : {'BrisCode': "pen", 'TrackType': "Thoroughbred", 'AtabCode': 'PEN',
                                 'NYRA': 'Penn National'},
              "Santa Anita Park" : {'BrisCode': "sa", 'TrackType': "Thoroughbred", 'AtabCode': 'SAD',
                                    'NYRA': 'Santa Anita'},
              # "Sunland Park" : {'BrisCode': "sun", 'TrackType': "Thoroughbred", 'AtabCode': 'SND',
              # not on NYRA                  'NYRA': 'Sunland Park'},
              "Turf Paradise" : {'BrisCode': 'tup', 'TrackType': "Thoroughbred", 'AtabCode': 'TUD',
                                 'NYRA': 'Turf Paradise'},
              "Turfway Park" : {'BrisCode': 'tp', 'TrackType': "Thoroughbred", 'AtabCode': 'TPD',
                                 'NYRA': 'Turfway Park'}
             }

def get_url(track, race_num = '1'):
    urls = {}
    win_show_url = "https://www.twinspires.com/adw/legacy/tote/wpsfullpools" \
                   "?username=my_tux&ip=0.0.0.0&affid=2800&affiliateId=2800" \
                   "&output=json&track=" + track_list[track]["BrisCode"] + "&type=" + \
                    track_list[track]["TrackType"] + "&race=" + str(race_num)

    schedule_url = "https://www.twinspires.com/adw/track/" + track_list[track]['AtabCode'] + \
                   "/race?username=my_tux&ip=0.0.0.0&affid=2800&affiliateId=2800&output=json"

    track_url = "https://www.twinspires.com/adw/track?username=my_tux&ip=0.0.0.0&affid=2800&affiliateId=2800" \
                "&output=json&includeGreyhound=true&state=NY"

    results_url = "https://www.twinspires.com/webapi/Tote/Results?username=my_tux&ip=0.0.0.0&affid=2800" \
                  "&affiliateId=2800&output=json&track=" + track_list[track]['BrisCode'] + \
                  "&type=" + track_list[track]['TrackType'] + "&race=" + str(race_num)

    exotic_pools_url = "https://www.twinspires.com/adw/legacy/tote/exoticpools" \
                   "?username=my_tux&ip=0.0.0.0&affid=2800&affiliateId=2800" \
                   "&output=json&track=" + track_list[track]["BrisCode"] + "&type=" + \
                    track_list[track]["TrackType"] + "&race=" + str(race_num)

    will_pays_url = "https://www.twinspires.com/adw/legacy/tote/willpays" \
                       "?username=my_tux&ip=0.0.0.0&affid=2800&affiliateId=2800" \
                       "&output=json&track=" + track_list[track]["BrisCode"] + "&type=" + \
                       track_list[track]["TrackType"] + "&race=" + str(race_num)
    race_url = "https://www.twinspires.com/adw/track/" + track_list[track]["AtabCode"] + \
               '/race?username=my_tux&ip=0.0.0.0&affid=2800&affiliateId=2800&output=json'

    urls = {'WPS'  : win_show_url,
          'Schedule' : schedule_url,
          'Results' : results_url,
          'Pools' : exotic_pools_url,
          'Will Pays' : will_pays_url,
          'Track' : track_url,
          'Races' : race_url}

    return urls

