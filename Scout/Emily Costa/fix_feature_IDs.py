from functions.emily import correct_prop_id as cpi 
import os
from os import path

csv_name = 'PropertyData.csv'
data_path = 'data_resources/yardi_property_data'
id_index = 'data_resources/id_index.csv'

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
                outpath = '' + dir + '/' + dir_city + '/'
                try:
                    cpi(inpath, id_index, save_csv=True, outfile_path=outpath, outfile_name=csv_name)
                except FileNotFoundError:
                    print(inpath, ' does not exist.')
                    
