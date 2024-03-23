import multiprocessing as mp
import datetime as dt
import pandas as pd
from os import path
import time
import os
'''
Author: Tiago Zanaga Da Costa
'''
# Fix time format from mm/dd/yyyy to yyyy-mm-dd
def fixTimeFormat(fpath):
    filein = pd.read_csv(fpath, index_col=0)
    dates = []
    index = filein.index
    # print(index[0])
    if(index[0] == '1/1/1950'):
        for i in index:
            # print(print(i[1]))
            if(i[1] != '/'):
                mm = '1' + i[1]
                dd = '0' + i[3]
                yyyy = i[5:9]
            else:
                mm = '0' + i[0]
                dd = '0' + i[2]
                yyyy = i[4:8]
            date = yyyy + '-' + mm + '-' + dd
            dates.append(date)
        filein.insert(loc=0, column='', value=dates)
        filein = filein.set_index('')
        filein.to_csv(fpath, sep=',', encoding='utf-8')

    return

def crawlDirectories(data_path):
    for root, dirs, files, in os.walk(data_path):
        for dir in dirs:
            for root_city, dirs_city, files_city in os.walk(path.join(root, dir)):
                for dir_city in dirs_city:
                    start = time.perf_counter()
                    or_fp = path.join(root_city, dir_city, "Occupancy Rate.csv")
                    ra_fp = path.join(root_city, dir_city, "Rent Actual.csv")
                    rm_fp = path.join(root_city, dir_city, "Rent Market.csv")
                    rpsfa_fp = path.join(root_city, dir_city, "Rent Per SqFt Actual.csv")
                    rpsfm_fp = path.join(root_city, dir_city, "Rent Per SqFt Market.csv")
                    ro_fps = [or_fp, ra_fp, rm_fp, rpsfa_fp, rpsfm_fp]
                    for fp in ro_fps:
                        fixTimeFormat(fp)
                    finish = time.perf_counter()
                    dur = round((finish - start), 4)
                    print(f"[DONE!] {root_city}/{dir_city}.\n"
                    + f"Duration (secs): {dur}")
def main():
    sePath = '../data_resources/fixed_data/SE'
    swPath = '../data_resources/fixed_data/SW'
    nePath = '../data_resources/fixed_data/NE'
    nwPath = '../data_resources/fixed_data/NW'
    mwPath = '../data_resources/fixed_data/MW'
    threads = list()
    seThread = mp.Process(target = crawlDirectories, args = (sePath,))
    swThread = mp.Process(target = crawlDirectories, args = (swPath,))
    neThread = mp.Process(target = crawlDirectories, args = (nePath,))
    nwThread = mp.Process(target = crawlDirectories, args = (nwPath,))
    mwThread = mp.Process(target = crawlDirectories, args = (mwPath,))
    threads.append(seThread)
    threads.append(swThread)
    threads.append(neThread)
    threads.append(nwThread)
    threads.append(mwThread)

    for thread in threads:
        thread.start()

    begin = time.perf_counter()
    for index, thread in enumerate(threads):
        print(f"Main : before joining thread {index}.")
        thread.join()
        print(f"Main : thread {index} done.")
    end = time.perf_counter()
    print(f"Total Duration: {end-begin}.")

main()
