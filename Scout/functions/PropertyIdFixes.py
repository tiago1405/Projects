'''
Version: 1.0.0
Date: 18/03/2020
Author: Tiago Zanaga Da Costa

Description:
____________
Program containing functions to fix property ID in Data CSVs by either:
    1) Fixing the existing property IDs by concatenating the market and submarket
    codes to them.
    2) Adding them to a CSV if not present by matching properties in said CSV
     with their counterparts in another CSV which contains property IDs using
     another indicator of similarity such as address or property name.
'''
import pandas as pd
import numpy as np
import os


class PropertyIDFixes:

    '''
    Description:
    ------------
    Add Property IDs to a data source which does not currently have the
    PROPERTY_ID column by matching properties to a master file containing
    the correct Property IDs through the Property's Address.

    Parameters:
    -----------
    fp_arr[]: string array
        Array containing the file paths to the:
        [0]: Master CSV (i.e.: PropertyData.csv) containing the correct Property
        IDs.
        [1]: File Inputted to Fix Indexes (fifi), the file which does not
        have the PROPERTY_ID column.

    indexByID: Boolean
        Bool indicating whether the returned Pandas DataFrame should be indexed
        by Property ID or numerically.

    Return:
    ------
    fifi_df: Pandas DataFrame
        The fixed Pandas DataFrame which now contains the PROPERTY_ID column,
        and/or is indexed by it.

    '''
    def addPropIDByAddress(fp_arr):
        # Read PropertyData (pd) CSV (csv with the propIDs) into a Pandas DF,
        # index Numerically by Entry
        pd_df = pd.read_csv(fp_arr[0])
        # Read the File Inputed to Fix Indices (fifi) excel into a Pandas DF,
        # index Numerically by Entry
        fifi_df = pd.read_excel(fp_arr[1])

        # Sort all Data Frames by their address and city in ascending order
        pd_df = pd_df.sort_values(by=['PROPERTY_ADDRESS', 'PROPERTY_CITY'], ascending=True)
        fifi_df = fifi_df.sort_values(by=['Address', 'City'], ascending=True)

        # Reset Indices
        pd_df = pd_df.reset_index()
        fifi_df = fifi_df.reset_index()

        # Drop junk and old index columns
        pd_df = pd_df.drop(['index', 'Unnamed: 0'], axis=1)
        fifi_df = fifi_df.drop(['index'], axis=1)

        # Create Pandas Series to store the property IDs to be
        # inserted into the DataFrames.
        fifi_ids = pd.Series([], dtype=str)

        c1 = 0

        print("PropertyData Len: ", len(pd_df))
        print("File In Len : ", len(fifi_df))
        for i in range(len(fifi_df)):
            for j in range(len(pd_df)):
                if fifi_df['Address'][i] == pd_df['PROPERTY_ADDRESS'][j]:
                    fifi_ids[c1] = pd_df['PROPERTY_ID'][j]
                    c1 += 1
                    break
                elif (j == len(pd_df) - 1):
                    print('ERROR[', c1, ']: Property not found in Master (PropertyData).',
                    'Filling with empty string: "".')
                    fifi_ids[c1] = ""
                    c1 += 1

        print('Done indexing!')
        print('fifi_ids len: ',len(fifi_ids), '\n')

        # Add Property_Id column to fifi dataframe
        fifi_df['PROPERTY_ID'] = fifi_ids
        # Reindex fifi_df by Property_Id
        fifi_df = fifi_df.set_index(fifi_ids)

        # print("PropertyData(Master): \n")
        # print(pd_df)
        # print("File In: \n")
        # print(fifi_df)

        return(fifi_df)

'''
Main used to test the class functions with two Excel files: PropertyLoans and
PropertySales.
'''

def main():
    # Current working Directory
    cwd = os.getcwd()
    cwd = cwd[:-9]

    ls_fp = cwd + "data_resources/yardi_property_data/Northern California/San Francisco/"
    pl_fp = ls_fp + "PropertyLoans (4).xlsx"
    ps_fp = ls_fp + "PropertySales (6).xlsx"

    pd_fp = cwd + "data_resources/fixed_feature/Northern California/San Francisco/"
    pd_fp += "PropertyData.csv"

    fp_arr1 = [pd_fp, pl_fp]
    fp_arr2 = [pd_fp, ps_fp]

    pl_fdf = pd.DataFrame()
    ps_fdf = pd.DataFrame()

    print('\nFixing PropertyLoans: \n')
    pl_fdf = PropertyIDFixes.addPropIDByAddress(fp_arr1)
    print('\nFixing PropertySales: \n')
    ps_fdf = PropertyIDFixes.addPropIDByAddress(fp_arr2)

    op_fp = cwd + "data_resources/fixed_series/Northern California/"
    fpl_fp = op_fp + "PropertyLoans (Fixed).csv"
    fps_fp = op_fp + "PropertySales (Fixed).csv"

    pl_fdf.to_csv(fpl_fp, sep=',', encoding='utf-8')
    ps_fdf.to_csv(fps_fp, sep=',', encoding='utf-8')
    return()


#main()
