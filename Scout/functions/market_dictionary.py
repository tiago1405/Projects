import pandas as pd
import numpy as np
import os as os


'''
Description: Create a SubmarketID Dictionary from a given PropertyData.csv file for an
individual market.

csv_fp = CSV File Path
Author: Tiago Da Costa
'''
def make_market_dict(csv_fp):

    # Read in the CSV file whose path is given into the pandas DataFrame: file_in
    file_in = pd.read_csv(csv_fp)
    # print(file_in)

    # Sort the Pandas DataFrame (file_in) by MARKET and SUBMARKET_CODE
    # (SUBMARKET_ID) in asecending order.
    file_in = file_in.sort_values(by=['MARKETID', 'SUBMARKET_CODE'], ascending=True)

    # Reset the indices of file_in that were messed around due to sorting the values.
    # Apply the Array (filter) to file_in and assign it to the DataFrame
    # (markets_df) to get a DataFrame of only the MARKETID, MARKETNAME,
    # SUBMARKET_CODE, and SUBMARKET_NAME.
    filter = ['MARKETID', 'MARKET_NAME', 'SUBMARKET_CODE', 'SUBMARKET_NAME']
    file_in = file_in.reset_index()
    markets_df = file_in[filter]

    # print(markets_df)

    # Create a set of tuples (set(tuples()) ) to store the submarkets and markets
    # from markets_df.
    # Note: I am using sets of tuples because sets automatically remove duplicate
    # values, and the tuple is the ((sub)market_name, (sub)market_id(code))
    submarkets = set(())
    markets = set(())
    for index, rowdata in markets_df.iterrows():
        submarkets.add((rowdata['SUBMARKET_NAME'], rowdata['SUBMARKET_CODE']))
        markets.add((rowdata['MARKET_NAME'], rowdata['MARKETID']))

    # Convert them to lists so that we can access them better
    list(markets)
    list(submarkets)

    # Sort both the submarkets and markets lists in ascending order using the
    # submarket_code field as the sorting key
    submarkets = sorted(submarkets, key = lambda x : x[1])
    markets = sorted(markets, key = lambda x : x[1])

    #Convert the lists to numpy arrays so we can use them in the DataFrames
    submarkets = np.array(submarkets)
    markets = np.array(markets)

    # Unzip the tuples so that we can add them with individual labels to the
    # new DataFrame: output_df. This will be the DataFrame we return to main().
    sub_name, sub_id = zip(*submarkets)
    output_df = pd.DataFrame({'SUBMARKET_NAME': sub_name, 'SUBMARKET_ID': sub_id})

    # Create the output file name: output_fn, using the markets data array to
    # send back to main for use in creating a CSV of output_df
    output_fn = str(markets[0,1]) + " " + markets[0,0]

    # Return the variables to main
    return output_df, output_fn

def main():
    # csv_fp = CSV File Path. The path of the CSV that will be loaded in
    csv_fp = os.getcwd()[:-9] + '/data_resources/yardi_property_data/Florida/Miami/'
    # csv_out_fp = CSV Output File Path. The path of the CSV outputted from this
    # function.
    csv_out_fp = ''
    # Concatenate PropertyData.csv to the loading File Path
    csv_fp += 'PropertyData.csv'
    # file_out_name = File Output Name. The name of the outputted CSV
    file_out_name = ''
    # File_out = File Out. It is the DataFrame that will be converted to a
    # CSV and outputted from main.
    file_out = pd.DataFrame()
    # Call the make_market_dict function to create the Dictionary DataFrame
    # and the File Output Name which is based off the market.
    file_out, file_out_name = make_market_dict(csv_fp)
    # print(file_out)
    # print(file_out_name)
    #  Output file_out as a CSV file and save it to csv_out_fp + file_out_name.
    # Separate by tabs and use utf-8 (the same as all our data) text encoding.
    for col in file_out.columns:
        print(col)
    file_out.to_csv(csv_out_fp + file_out_name + ".csv", sep=',', encoding='utf-8')

main()
