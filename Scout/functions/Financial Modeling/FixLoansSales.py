import sys
sys.path.insert(1, '../functions')
from FeatureSupportFunctions import FeatureSupportFunctions as fsf
from PropertyIdFixes import PropertyIDFixes as pidfix
import pandas as pd
import os as os
import warnings
import threading
import multiprocessing as mp
import logging
from os import path
'''
Author: Tiago Zanaga Da Costa
'''

data_path = '../data_resources/fixed_data'

def crawlSales():
    for root, dirs, files, in os.walk(data_path):
        for dir in dirs:
            for root_city, dirs_city, files_city in os.walk(path.join(root, dir)):
                for dir_city in dirs_city:
                    pdata_path = path.join(root_city, dir_city, 'PropertyData.csv')
                    occr8_path = path.join(root_city, dir_city, 'Occupancy Rate.csv')
                    sales_path = path.join(root_city, dir_city, 'PropertySales.xlsx')
                    loans_path = path.join(root_city, dir_city, 'PropertyLoans.xlsx')
                    sales_am_path = path.join(root_city, dir_city, 'Sales Amount.csv')
                    print(pdata_path)
                    fp1 = [pdata_path, sales_path]
                    fp2 = [pdata_path, loans_path]
                    pd_df = pd.read_csv(pdata_path, index_col=1)
                    or_df = pd.read_csv(occr8_path, index_col=0)
                    prop_ids = pd_df.index
                    index = or_df.index
                    dates = []
                    for i in index:
                        dates.append(pd.Timestamp(i))
                    ps_df = pidfix.addPropIDByAddress(fp1)
                    pl_df = pidfix.addPropIDByAddress(fp2)
                    # Calculate the hit rage for loans and sales on PropertyIDs
                    ps_hr = fsf.df_hit_rate(ps_df, prop_ids)
                    pl_hr = fsf.df_hit_rate(pl_df, prop_ids)
                    ps_ids = fsf.df_hit_list(ps_df, prop_ids)
                    pl_ids = fsf.df_hit_list(pl_df, prop_ids)
                    sales_amount = pd.DataFrame(index=dates, columns=prop_ids)
                    ''' Extract Sale Price (amount) from Loans and Sales dfs
                    and re-structure to be time indexed.                '''
                    fsf.extract_sales_amount(dates, ps_ids, pl_ids, ps_df, pl_df, sales_amount)
                    sales_amount.to_csv(sales_am_path, sep=',', encoding='utf-8')
                    print('DONE WITH SALES FOR', dir_city)


def crawlLoans():
    for root, dirs, files, in os.walk(data_path):
        for dir in dirs:
            for root_city, dirs_city, files_city in os.walk(path.join(root, dir)):
                for dir_city in dirs_city:
                    pdata_path = path.join(root_city, dir_city, 'PropertyData.csv')
                    occr8_path = path.join(root_city, dir_city, 'Occupancy Rate.csv')
                    sales_path = path.join(root_city, dir_city, 'PropertySales.xlsx')
                    loans_path = path.join(root_city, dir_city, 'PropertyLoans.xlsx')
                    loans_am_path = path.join(root_city, dir_city, 'Loans Amount.csv')
                    print(pdata_path)
                    fp1 = [pdata_path, sales_path]
                    fp2 = [pdata_path, loans_path]
                    pd_df = pd.read_csv(pdata_path, index_col=1)
                    or_df = pd.read_csv(occr8_path, index_col=0)
                    prop_ids = pd_df.index
                    index = or_df.index
                    dates = []
                    for i in index:
                        dates.append(pd.Timestamp(i))
                    ps_df = pidfix.addPropIDByAddress(fp1)
                    pl_df = pidfix.addPropIDByAddress(fp2)
                    # Calculate the hit rage for loans and sales on PropertyIDs
                    ps_hr = fsf.df_hit_rate(ps_df, prop_ids)
                    pl_hr = fsf.df_hit_rate(pl_df, prop_ids)
                    ps_ids = fsf.df_hit_list(ps_df, prop_ids)
                    pl_ids = fsf.df_hit_list(pl_df, prop_ids)
                    loans_amount = pd.DataFrame(index=dates, columns=prop_ids)
                    ''' Extract Loan Amount from Loans and Sales dfs and
                    restructure to be time indexed                      '''
                    fsf.extract_loan_amount(dates, ps_ids, pl_ids, ps_df, pl_df, loans_amount)
                    loans_amount.to_csv(loans_am_path, sep=',', encoding='utf-8')
                    print('DONE WITH LOANS FOR', dir_city)


def crawlRatesDuration():
    for root, dirs, files, in os.walk(data_path):
        for dir in dirs:
            for root_city, dirs_city, files_city in os.walk(path.join(root, dir)):
                for dir_city in dirs_city:
                    pdata_path = path.join(root_city, dir_city, 'PropertyData.csv')
                    occr8_path = path.join(root_city, dir_city, 'Occupancy Rate.csv')
                    sales_path = path.join(root_city, dir_city, 'PropertySales.xlsx')
                    loans_path = path.join(root_city, dir_city, 'PropertyLoans.xlsx')
                    duration_path = path.join(root_city, dir_city, 'Loans Duration.csv')
                    rates_path = path.join(root_city, dir_city, 'Loans Rates.csv')
                    print(pdata_path)
                    fp1 = [pdata_path, sales_path]
                    fp2 = [pdata_path, loans_path]
                    pd_df = pd.read_csv(pdata_path, index_col=1)
                    or_df = pd.read_csv(occr8_path, index_col=0)
                    prop_ids = pd_df.index
                    index = or_df.index
                    dates = []
                    for i in index:
                        dates.append(pd.Timestamp(i))
                    ps_df = pidfix.addPropIDByAddress(fp1)
                    pl_df = pidfix.addPropIDByAddress(fp2)
                    # Calculate the hit rage for loans and sales on PropertyIDs
                    ps_hr = fsf.df_hit_rate(ps_df, prop_ids)
                    pl_hr = fsf.df_hit_rate(pl_df, prop_ids)
                    ps_ids = fsf.df_hit_list(ps_df, prop_ids)
                    pl_ids = fsf.df_hit_list(pl_df, prop_ids)
                    loan_duration = pd.DataFrame(index=dates, columns=prop_ids)
                    loan_rate = pd.DataFrame(index=dates, columns=prop_ids)
                    ''' Extract Loan Rate and Loan Duration from Loans df
                    and restructure to be time indexed                  '''
                    fsf.extract_rate_duration(dates, pl_ids, pl_df, loan_rate, loan_duration)
                    loan_duration.to_csv(duration_path, sep=',', encoding='utf-8')
                    loan_rate.to_csv(rates_path, sep=',', encoding='utf-8')
                    print('DONE WITH RATES AND DURATIONS FOR', dir_city)


def main():
    threads = list()
    saThread = mp.Process(target = crawlSales,
    args = ())
    laThread = mp.Process(target = crawlLoans,
    args = ())
    rdThread = mp.Process(target = crawlRatesDuration,
    args = ())

    threads.append(saThread)
    threads.append(laThread)
    threads.append(rdThread)
    for thread in threads:
        thread.start()

    for index, thread in enumerate(threads):
        logging.info("Main : before joining thread %d.", index)
        thread.join()
        logging.info("Main : thread %d done.", index)

main()
