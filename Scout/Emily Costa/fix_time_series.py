from functions.market_dictionary import make_market_dict as mmd
from functions.emily import iterate_dir as itdir
import pandas as pd
from os import path
import os

# Make submarkets dictionary for all data.
output_df = pd.DataFrame(columns=['SUBMARKET_NAME', 'SUBMARKET_ID'])
temp_df = pd.DataFrame()
output_fn = ''
csv_name = 'PropertyData.csv'
data_path = 'data_resources/yardi_property_data'

verbose=False

for root, dirs, files in os.walk(data_path):
    # Iterate through all regional directories.
    for dir in dirs:
        # Iterate through all city directories.
        for root_city, dirs_city, files_city in os.walk(path.join(root, dir)):
            for dir_city in dirs_city: # Each dir_city is a cities' info.
                try:
                    os.makedirs('' + dir + '/' + dir_city)
                except FileExistsError:
                    if verbose:
                        print('File exists')
                inpath = path.join(root_city, dir_city, csv_name)
                try:
                    temp_df, output_fn = mmd(inpath)
                    output_df = pd.concat([output_df,temp_df], ignore_index=True)
                    print(output_fn, ' has been appended the dataframe.')
                except FileNotFoundError:
                    print(inpath, ' does not exist.')
print(output_df)

id_index = 'data_resources/id_index.csv'
output_df.to_csv(id_index)
filename = 'RentAndOccupancyData.csv'

itdir(data_path, filename, id_index)