from CsvWriter import *
import time
# This portion of the code is in the task scheduler

if __name__ == '__main__':
    for track in track_list.keys():
        try:
            track_data_collector(track)
        except:
            pass
