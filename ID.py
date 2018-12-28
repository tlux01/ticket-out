
track_list = {
              "Aqueduct": {'BrisCode': "aqu", "TrackType": "Thoroughbred", 'AtabCode': 'AQD'},
              "Churchill Downs": {'BrisCode': "CD", "TrackType": "Thoroughbred", 'AtabCode': None},
              "Del Mar": {'BrisCode': "DMR", "TrackType": "Thoroughbred", 'AtabCode': None},
              "Fair Grounds": {'BrisCode': 'fg', 'TrackType': 'Thoroughbred', 'AtabCode': 'JGD'},
              "Gulfstream Park": {'BrisCode': "gp", "TrackType": "Thoroughbred", 'AtabCode': "GPM"},
              "Hawthorne": {'BrisCode': "haw", "TrackType": "Thoroughbred", 'AtabCode': "HAD"},
              "Laurel Park": {'BrisCode': "lrl", 'TrackType': "Thoroughbred", 'AtabCode': 'LRM'},
              "Test": ["lim", "Thoroughbred"],
              "The Meadows": ["MEA", "Harness"]
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

