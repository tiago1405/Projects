from modelFeatGeneration import FeatureGenerationFunctions as fgf
import multiprocessing as mp
import logging as logging
from os import path
import numpy as np
import os as os
import time

'''
Version: 1.1.0
Date: 08/07/2020
Author: Tiago Zanaga Da Costa

Main for csv_interpolation and model_formulas. Used to infer data points
and create new features from pre-existing real estate data.

wdir_p = Working Directory Path = /home/$USER/Documents/saffron_capital
dir_p = Directory Path
pd_dir_p = PopertyData Directory Path
'''

def crawlDirectories(data_path):
    for root, dirs, files, in os.walk(data_path):
        for dir in dirs:
            for root_city, dirs_city, files_city in os.walk(path.join(root, dir)):
                for dir_city in dirs_city:
                    start = time.perf_counter()
                    output_path = path.join(root_city, dir_city, dir_city+" Model.csv")
                    print(f"[START] {root_city}/{dir_city}")
                    if path.exists(output_path):
                        print('Model Already Exists!')
                    else:
                        or_fp = path.join(root_city, dir_city, "Occupancy Rate.csv")
                        ra_fp = path.join(root_city, dir_city, "Rent Actual.csv")
                        rm_fp = path.join(root_city, dir_city, "Rent Market.csv")
                        rpsfa_fp = path.join(root_city, dir_city, "Rent Per SqFt Actual.csv")
                        rpsfm_fp = path.join(root_city, dir_city, "Rent Per SqFt Market.csv")
                        ro_fps = [or_fp, ra_fp, rm_fp, rpsfa_fp, rpsfm_fp]

                        pd_fp = path.join(root_city, dir_city, "PropertyData.csv")
                        sa_fp = path.join(root_city, dir_city, "Sales Amount.csv")
                        la_fp = path.join(root_city, dir_city, "Loans Amount.csv")
                        ld_fp = path.join(root_city, dir_city, "Loans Duration.csv")
                        lr_fp = path.join(root_city, dir_city, "Loans Rates.csv")
                        aux_fps = [pd_fp, sa_fp, la_fp, ld_fp, lr_fp]

                        fgf.GenerateFeatures(ro_fps, aux_fps, output_path)
                    finish = time.perf_counter()
                    dur = round((finish - start), 4)
                    print(f"[DONE!] {root_city}/{dir_city}.\n"
                    + f"Duration (secs): {dur}")
    return()

def monoThreaded():
    data_path = '../data_resources/fixed_data'
    newModels(data_path)

def multiThreaded():
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
    # mwThread = mp.Process(target = crawlDirectories, args = (mwPath,))
    threads.append(seThread)
    threads.append(swThread)
    threads.append(neThread)
    threads.append(nwThread)
    # threads.append(mwThread)

    for thread in threads:
        thread.start()

    begin = time.perf_counter()
    for index, thread in enumerate(threads):
        print(f"Main : before joining thread {index}.")
        thread.join()
        print(f"Main : thread {index} done.")
    end = time.perf_counter()
    print(f"Total Duration: {end-begin}.")
    return()

def newModels(data_path):
    done = []
    # Load the file with processed markets and edit them to remove the newline char
    if path.isfile('done.txt'):
        done_file = open('done.txt', 'r')
        done = done_file.readlines()
        done_file.close()
        for i in range(0, len(done)):
            done[i] = done[i][:-1]

    try:
        for root, dirs, files, in os.walk(data_path):
            for dir in dirs:
                for root_city, dirs_city, files_city in os.walk(path.join(root, dir)):
                    for dir_city in dirs_city:
                        # Start the timer
                        start = time.perf_counter()
                        # Check if the current city has been previously completed
                        if path.join(root_city, dir_city) not in done:
                            print(f"[START] {root_city}/{dir_city}")
                            model_path = path.join(root_city, dir_city, dir_city+" Model.csv")
                            market_path = path.join(root_city, dir_city, dir_city+"_market_data.csv")
                            fgf.newDataGen(model_path, market_path, model_path)
                            print(f"[DONE!] {root_city}/{dir_city}.")
                            done.append(path.join(root_city, dir_city))
                        # If it has print skip it and print that it has
                        else:
                            print(f"[EXCEPT] {root_city}/{dir_city} had already been done.")
                        # Timer end
                        finish = time.perf_counter()
                        # Calculate time elapsed and round to 4 decimal points then print
                        dur = round((finish - start), 4)
                        print(f"Duration (secs): {dur}")

    except Exception as inst:
        print()
        print(f'[ERROR] Type: {type(inst)}')
        print(f'[ERROR] Args: {inst.args}')
        print(f'[ERROR] : {inst}')
        # Save/Update file of the markets that have been processed
        with open('done.txt', 'w') as f:
            for item in done:
                f.write("%s\n" % item)

    return()
# threadedExecution()
monoThreaded()
# newModels()
