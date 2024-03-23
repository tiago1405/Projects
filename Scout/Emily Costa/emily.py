"""
A library of functions for the purpose of data engineering.

Functions Descriptions
----------------------
combine_csv:            Function to interpolate datasets (csv) into one csv file.
clean_data:
seperate_series:        For seperating series properties into different CSV files.
correct_prop_id:        For correcting property IDs by appending submarket and fixing format.
time_series_as_index:   Sets column headers of input file as the index of output file.
iterate_dir:            Iterate through directories and fix property IDs, seperate the series
                        data and set time series as the index.

Created on: January 21, 2020
Written by: Emily Costa
"""

import pandas as pd
import random
from os import path
import warnings
import os

def combine_csv(files, columns, output_file_name, verbose = False):
    """
    Function to interpolate datasets (csv) into one csv file.

    Parameter
    ---------
    files: dictionary, string : string or array of strings
        (key) The path/to/desired/files for which the data will be extracted.
        (value) The columns to use to match the rows.
    columns: dictionary, string : string or array of strings
        (key) The path/to/desired/files for which the data will be extracted.
        (value) The columns to add to new dataset.
        name_of_file : name_of_columns
    output_file_name: string
        Name of CSV to save final dataframe to.
    verbose: bool, optional
        Whether or not to print debugging statements.

    Returns
    -------
    Null
    """

    # Check for current types of parameters
    if not isinstance(files, (dict)):
        raise TypeError('The filenames must be in a Python list.')
    if not isinstance(columns, (dict)):
        raise TypeError('The columns you want to combine must be a Python dictionary strings for both the key and value (name_of_file : name_of_columns).')
    if not isinstance(output_file_name, (str)):
        raise TypeError('The input of the name for the final CSV must be a string.')
    #if not chdir is None:
    #    if not isinstance(chdir, (str)):
    #        raise TypeError('The path of the location to save the final file must be a string')
    if verbose:
        print('All parameter inputs are of the correct type.')

    # Check that the dictionaries has the correct data and types.
    for key in files.keys():
        if not path.exists(key):
            raise OSError('The following path does not exist in files dict:' + key)
        if not path.isfile(key):
            raise OSError('The following path must be a file in files dict:' + key)
        if not isinstance(key, (str)):
            raise TypeError('All keys in files must be a string. This is not: ' + key)
        if not isinstance(files[key], (str)):
            if isinstance(files[key], (list, tuple)):
                if not all(isinstance(col,(str)) for col in files[key]):
                    raise TypeError('Not all the values in the following files key are strings: ' + key)
            else:
                raise TypeError('The value in the following files key is not a string: ' + key)
    for key in columns.keys():
        if not path.exists(key):
            raise OSError('The following path does not exist in column dict:' + key)
        if not path.isfile(key):
            raise OSError('The following path must be a file in column dict:' + key)
        if not isinstance(key, (str)):
            raise TypeError('All keys in columns must be a string. This is not: ' + key)
        if not isinstance(files[key], (str)):
            if isinstance(files[key], (list, tuple)):
                if not all(isinstance(col,(str)) for col in files[key]):
                    raise TypeError('Not all the values in the following columns key are strings: ' + key)
            else:
                raise TypeError('The value in the following columns key is not a string: ' + key)
    if verbose:
        print('The dictionaries have the correct keys and values.')

    # 1. Add matching data to new dataset
    # Choose a random file_name and its values that are for matching
    random_file = random.choice(list(files.keys()))
    if verbose:
        print('The columns designated for matching the datasets are: ' + files.get(random_file, ""))
    # Create a new csv from the key : values and the column data
    match = [files.get(random_file, "")]
    match_path = path.join(path.expanduser('~'), os.getcwd(), random_file)
    cum_df = pd.read_csv(match_path, usecols=match)
    print(columns)
    # 2. Iterate through all file_names and add the desired column data to cum_df.
    for file_name, matching_row in files.items():
        f_path = path.join(path.expanduser('~'), os.getcwd(), file_name)
        file_df = pd.read_csv(f_path)
        # Take matching columns and desired columns and make new dataframe.
        cols = [matching_row]
        print(file_name)
        if isinstance(columns[file_name], (list, tuple)):
            for row in columns[file_name]:
                cols.append(row)
        else:

            # l = cols[file_name]
            cols.append(columns[file_name])
        file_df = file_df[columns]
        if verbose:
            print(file_df)
        # Raise warning if a desired column is not found but continue interpolation.
        if not matching_row in file_df:
            warnings.warn(matching_row + ' does not exist in ' + file_name, Warning)
        else: # Do the step
            cum_df = cum_df.merge(file_df, how='left', left_on=match, right_on=matching_row)

    # 3. Save cum_df as a csv
    # Change directory if user wants to save file elsewhere.
    cum_df.to_csv(output_file_name)

def clean_data():
    """

    Parameters
    ----------

    Return
    ------

    """

def seperate_series(infile_path, save_csv = False, outfile_path = './', outfile_name = '',
                        verbose = False):
    """
    For seperating series properties into different CSV files.
    Format of outfiles:
    Filename       - series_property_name
    Column Headers - dates
    Row Headers    - property_idea

    Parameters
    ----------
    infile_path: string
        Path to the file to be separeted.
    save_csv: bool, optional
        Set True to save new dataframes to csv. Default is False.
    outfile_path: string, optional
        Directory where output files will be saved.
        Default is in current directory.
    outfile_name: string, optional
        Name of output files will be outfile_name + series.
        Default is empty so names will just be series.
    verbose: bool, optional
        Default is False. Set True for debugging statements.

    Return
    ------
    A dataframe with series_type : data.
    A list of filenames.
    """
    # Check parameter for type errors
    #if not isinstance(infile_path, (str)):
    #    raise TypeError('infile_path should be a string.')
    if not isinstance(outfile_path, (str)):
        raise TypeError('outfile_path should be a string.')
    if not isinstance(outfile_name, (str)):
        raise TypeError('outfile_name should be a string.')
    if not isinstance(save_csv, (bool)):
        raise TypeError('save_csv should be a boolean, True or False')
    if not isinstance(verbose, (bool)):
        raise TypeError('verbose should be a boolean, True or False')
    if verbose:
        print('All parameters are of the correct type.')

    # Open input file and convert to pandas dataframe
    input_file = open(infile_path)
    input_df = pd.read_csv(input_file)

    # To be verbose, show the types of series that exist in file.
    series_names = input_df['SERIES'].drop_duplicates()
    if verbose:
        print(series_names)

    # Make a dictionary that separates the series types by group.
    dict_of_series = {k: v for k, v in input_df.groupby('SERIES')}
    if verbose:
        print(dict_of_series)

    # Dictionary for function to return
    all_dfs = pd.Series(dict_of_series)
    # Figure out how to drop for this part: ???
    # all_dfs = all_dfs.drop(['MARKET_NAME','SUBMARKET_NAME','PROPERTY_NAME','SERIES'], axis=1)

    # In case of saving to separate CSVs
    fn = ''
    fns = []
    if save_csv:
        for key, val in dict_of_series.items():
            t_df = pd.DataFrame.from_dict(val)
            if verbose:
                print(t_df)
            t_df = t_df.drop(['MARKET_NAME','SUBMARKET_NAME','PROPERTY_NAME','SERIES'], axis=1)
            fn = outfile_path + outfile_name + '_' + key + '.csv'
            fns.append(fn)
            t_df.to_csv(fn)
        return fns

    return all_dfs, fns


def correct_prop_id(infile_path, id_index, save_csv = False, outfile_path = './',
                        outfile_name = None, verbose = False):
    """
    For correcting property IDs by appending submarket and fixing format.
    Format of property ID: abc-def-ghijk
    abc:   market
    def:   submarket
    ghijk: property

    Parameters
    ----------
    infile_path: string
        Path to the file to be separeted.
    id_index: string
        Path to the file that contains indexes to match property
        ID with property information.
    save_csv: bool, optional
        Set True to save new dataframes to csv. Default is False.
    outfile_path: string, optional
        Directory where output files will be saved.
        Default is in current directory.
    outfile_name: string, optional
        Rename the infile to outfile_name.
        Default is empty so name will be same as infile name.
    verbose: bool, optional
        Default is False. Set True for debugging statements.

    Return
    ------
    A dataframe with corrected property IDs if not saving to csv.
    The path/to/saved_csv.csv if saving to csv.
    """
    # Check parameters for error types.
    if not isinstance(infile_path, (str)):
        raise TypeError('infile_path should be a string.')
    if not isinstance(id_index, (str)):
        raise TypeError('id_index should be a string.')
    if not isinstance(outfile_path, (str)):
        raise TypeError('outfile_path should be a string.')
    #if not isinstance(outfile_name, ((str, None))):
    #    raise TypeError('outfile_name should be a string.')
    if not isinstance(save_csv, (bool)):
        raise TypeError('save_csv should be a boolean, True or False')
    if not isinstance(verbose, (bool)):
        raise TypeError('verbose should be a boolean, True or False')
    if verbose:
        print('All parameters are of the correct type.')

    # Open input file and convert to pandas dataframe.
    input_file = open(infile_path)
    input_df = pd.read_csv(input_file)

    # Open id_index file and convert to pandas dataframe.
    index_file = open(id_index)
    index_df = pd.read_csv(index_file)

    # Iterate through each item in property ID columns.
    for index, row in input_df.iterrows():
        # Find submarket ID number in id_index using submarket name.
        try:
            sub_id_df = index_df.loc[index_df['SUBMARKET_NAME'] == row['SUBMARKET_NAME']]
        except KeyError:
            return 'Submarket ID missing for ', input_file
        # sub_id_df.to_csv('please_work.csv')
        sub_id = sub_id_df.iat[0,2]
        if verbose:
            print('Submarket ID of property ', row[0], ' is ', sub_id)
        # Append submarket ID number to property ID
        sub_id = str(sub_id)
        # If ID is only 1 digit, make into 2 digits.
        if(len(sub_id) < 2):
            sub_id = '0' + sub_id
        input_df.at[index, 'PROPERTY_ID'] = row['PROPERTY_ID'] + '_' + sub_id

    if verbose:
        print('Final dataframe: \n', input_df)

    # Save fixed property id to new CSV.
    if save_csv:
        #if outfile_name is None:
        #    outfile_name = infile_path
        input_df.to_csv(outfile_path + outfile_name)
        return outfile_path + outfile_name

    # Return dataframe containing fixed property IDs
    return input_df

def time_series_as_index(infile_path, save_csv = False, outfile_path = './',
                            outfile_name = None, verbose = False):
    '''
    Sets column headers of input file as the index of output file.
    Note: column headers become the property IDs.

    Parameters
    ----------
    infile_path: string
        Path to the file to be manipulated.
    save_csv: bool, optional
        Set True to save new dataframes to csv. Default is False.
    outfile_path: string, optional
        Directory where output files will be saved.
        Default is in current directory.
    outfile_name: string, optional
        Name of output files will be outfile_name + series.
        Default is empty so names will just be series.
    verbose: bool, optional
        Default is False. Set True for debugging statements.

    Returns
    -------
    Dataframe with time series as index if not saving to csv.
    The path/to/saved_csv.csv if saving to csv.
    '''
    # Check parameter for type errors
    if not isinstance(infile_path, (str)):
        raise TypeError('infile_path should be a string.')
    if not isinstance(outfile_path, (str)):
        raise TypeError('outfile_path should be a string.')
    #if not isinstance(outfile_name, (str,None)):
    #    raise TypeError('outfile_name should be a string.')
    if not isinstance(save_csv, (bool)):
        raise TypeError('save_csv should be a boolean, True or False')
    if not isinstance(verbose, (bool)):
        raise TypeError('verbose should be a boolean, True or False')
    if verbose:
        print('All parameters are of the correct type.')

    # Open input file and convert to pandas dataframe.
    input_file = open(infile_path)
    input_df = pd.read_csv(input_file)

    # Drop unnamed columns.
    input_df = input_df.loc[:, ~input_df.columns.str.contains('^Unnamed')]

    # Transpose dataframe.
    input_df = input_df.transpose()

    # Drop old index and make new header.
    new_header = input_df.iloc[0] #grab the first row for the header
    input_df = input_df[1:] #take the data less the header row
    input_df.columns = new_header #set the header row as the df header

    # Set dates as index
    # input_df.rename(columns={'PROPERTY_ID': 'Date'}, inplace=True)
    #input_df
    #input_df.set_index('Date')

    # If user wants to save the dataframe as a CSV, save and return the path to CSV.
    if save_csv:
        if outfile_name is None:
            input_df.to_csv(infile_path)
            return infile_path
        else:
            input_df.to_csv(outfile_path + outfile_name)
            return outfile_path + outfile_name

    return input_df

def iterate_dir(data_path, filename, id_index, verbose=True):
    '''
    Iterate through directories and fix property IDs, seperate the series
    data and set time series as the index.

    Parameters
    ----------
    dir_path: string
        Path to the directory containing all market series data.'
    filename: string
        Name of file to be manipulated.
    verbose: bool, optional
        Set True for debugging statements.

    Returns
    -------
    Null
    '''

    # Check parameters.
    if not isinstance(data_path, (str)):
        raise TypeError('data_path should be a string.')
    if not isinstance(filename, (str)):
        raise TypeError('filename should be a string.')
    if not isinstance(verbose, (bool)):
        raise TypeError('verbose should be a boolean, True or False')
    if verbose:
        print('All parameters are of the correct type.')

    for root, dirs, files in os.walk(data_path):
        # Iterate through all regional directories.
        for dir in dirs:
            # Iterate through all city directories.
            for root_city, dirs_city, files_city in os.walk(path.join(root, dir)):
                for dir_city in dirs_city: # Each dir_city is a cities' info.
                    if verbose:
                        print(path.join(root_city, dir_city, filename))
                    # Set paths and make directories if needed.
                    infile_path = path.join(root_city, dir_city, filename)
                    outfile_path = path.join('/home/chach1/Documents/saffron_capital/data_resources/fixed_data/', dir, dir_city)
                    # outfile = path.join(outfile_path, filename)
                    # Fix all property IDs.
                    outfile = correct_prop_id(infile_path, id_index, outfile_path=outfile_path, outfile_name=filename, save_csv=True)
                    # Seperate the series.
                    infile_paths = seperate_series(outfile, outfile_path=outfile_path, outfile_name='', save_csv=True)
                    # Set index to be time series.
                    for infile_path in infile_paths:
                        print(infile_path)
                        time_series_as_index(infile_path, save_csv=True)
    return None

if __name__ == '__main__':
    infile_path = ''
    id_index = '../data_resources/samples/sample_submarket_index.csv'

    # test combine_csv
    '''
    loan_path = os.path.join(os.path.expanduser('~'),'Documents',
            'saffron_capital','data_resources','samples','loans_sample.csv')
    prop_path = os.path.join(os.path.expanduser('~'),'Documents',
            'saffron_capital','data_resources','samples','property_data_sample.csv')

    files = {loan_path : 'Address', prop_path : 'PROPERTY_ADDRESS'}
    columns = {loan_path : 'Market', prop_path : 'PROPERTY_ID'}
    output_file = 'sample_fixed.csv'
    combine_csv(files, columns, output_file, verbose=True)
    '''

    # test seperate_series
    '''
    sep = seperate_series('../data_resources/samples/emily_is_lazy.csv', outfile_path='../data_resources/fixed_samples/', outfile_name='Bay Area')
    print(sep.keys())
    '''

    # test correct_prop_id
    '''
    new_df = correct_prop_id(infile_path, id_index, save_csv=True)
    print(new_df)
    seperate_series(new_df, outfile_path='../data_resources/fixed_samples/', outfile_name='Bay Area', save_csv=True)
    '''

    # test iterate_dir
    '''
    iterate_dir('../data_resources/yardi_property_data', 'RentAndOccupancyData.csv')
    '''

    # test set_index
    '''
    df = time_series_as_index(infile_path, save_csv=False)
    df.to_csv('test.csv')
    data_top = df.head()
    for row in data_top.index:
        print(row, end = " ")
    '''
