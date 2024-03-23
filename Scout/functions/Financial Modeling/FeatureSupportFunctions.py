import pandas as pd
from datetime import datetime as dt
'''
Author: Tiago Zanaga Da Costa
'''

'''
Loans CSV:
    Index(['Market', 'Property Name', 'Address', 'City', 'State', 'ZIP', 'Units',
   'Impr. Rating', 'Loc. Rating', 'Owner', 'Completion Date',
   'Associated Sale Date', 'Associated Sale Price (MM)', 'Loan Type',
   'Loan Status', 'Lender Type', 'Loan Origination Date',
   'Loan Maturity Date', 'Loan Duration', 'Loan Amount (MM)',
   'Interest Rate %', 'Interest Type', 'Lender', 'Originator',
   'Sale/Loan Comments', 'Latitude', 'Longitude', 'PROPERTY_ID']

Sales CSV:
    Index(['Market', 'Property Asset Class', 'Property Name', 'Address', 'City',
   'State', 'ZIP', 'Unit Count', 'Completion Date', 'Impr. Rating',
   'Loc. Rating', 'Buyer', 'Seller', 'Sale Date', 'Sale Type',
   'Total Sale Price (MM)', 'Sale Price Per SqFt', 'Sale Price Per Unit',
   'Loan Maturity Date', 'Loan Amount (MM)', 'Latitude', 'Longitude',
   'PROPERTY_ID']
'''
class FeatureSupportFunctions:

    def df_hit_rate(df, prop_ids):

        # In DataFrame
        indf = 0
        # Not In DataFrame
        nindf = 0

        for prop in prop_ids:
            if(df['PROPERTY_ID'].isin([prop]).any()):
                # print('++ Found in DataFrame!: ' + prop)
                indf += 1
            else:
                nindf += 1
                # print('-- Not Found in DataFrame!: ' + prop)
        return(((indf/(indf+nindf))*100))

    def df_hit_list(df, prop_ids):

        # In DataFrame
        indf = 0
        # Not In DataFrame
        nindf = 0
        # Array of PropertyIDs that hit
        hitIDs = []

        for prop in prop_ids:
            if(df['PROPERTY_ID'].isin([prop]).any()):
                # print('++ Found in DataFrame!: ' + prop)
                hitIDs.append(prop)
                indf += 1
            else:
                nindf += 1
                # print('-- Not Found in DataFrame!: ' + prop)

        return(hitIDs)

    '''
    dates = A list of dates for the file
    ids1 = IDs for the Sales Dataset
    ids2 = IDs for the Loans Dataset
    indf1 = Sales Dataset
    indf2 = Loans Dataset
    outdf = The Datframe to be outputted to
    '''
    def extract_sales_amount(dates, ids1, ids2, indf1, indf2, outdf):
        # Sales Dataset
        for date in dates:
            print("ExtractSales Sales : ", date)
            # print(type(date))
            # For every timestep
            for prop in ids1:
                # For each property
                # Swapped from str to pandas._libs.tslibs.timestamps.Timestamp
                if(type(indf1.loc[prop]['Sale Date']) == pd._libs.tslibs.timestamps.Timestamp):
                    if(date >= indf1.loc[prop]['Sale Date'] and
                    type(outdf.loc[date][prop]) == float):
                        # print("Single Entry not in outdf")
                        outdf[prop][date] = indf1.loc[prop]['Total Sale Price (MM)']

                elif(type(indf1.loc[prop]['Sale Date']) == pd.core.series.Series):
                    for i in range(0, len(indf1.loc[prop]['Sale Date'])):
                        if(type(indf1.loc[prop]['Sale Date'][i]) != float and
                        date >= indf1.loc[prop]['Sale Date'][i] and
                        type(outdf.loc[date][prop]) == float):
                            # print("Series Entry not in outdf ", i)
                            outdf[prop][date] = indf1.loc[prop]['Total Sale Price (MM)'][i]
        # # Loans Dataset
        # for date in dates:
            print("ExtractSales Loans: ", date)
            # print(type(date))
            for prop in ids2:
                # For each property
                # Swapped from str to pandas._libs.tslibs.timestamps.Timestamp
                if(type(indf2.loc[prop]['Associated Sale Date']) == pd._libs.tslibs.timestamps.Timestamp):
                    if(date >= indf2.loc[prop]['Associated Sale Date'] and
                    type(outdf.loc[date][prop]) == float):
                        # print("Single Entry not in outdf")
                        outdf[prop][date] = indf2.loc[prop]['Associated Sale Price (MM)']

                elif(type(indf2.loc[prop]['Associated Sale Date']) == pd.core.series.Series):
                    for i in range(0, len(indf2.loc[prop]['Associated Sale Date'])):
                        if(type(indf2.loc[prop]['Associated Sale Date'][i]) != float and
                        date >= indf2.loc[prop]['Associated Sale Date'][i] and
                        type(outdf.loc[date][prop]) == float):
                            # print("Series Entry not in outdf ", i)
                            outdf[prop][date] = indf2.loc[prop]['Associated Sale Price (MM)'][i]
        return()

    '''
    dates = A list of dates for the file
    ids1 = IDs for the Sales Dataset
    ids2 = IDs for the Loans Dataset
    indf1 = Sales Dataset
    indf2 = Loans Dataset
    outdf = The Datframe to be outputted to
    '''
    def extract_loan_amount(dates, ids1, ids2, indf1, indf2, outdf):
        # Sales Dataset
        for date in dates:
            print("ExtractLoans Sales: ", date)
            for prop in ids1:
                # For each property
                if(type(indf1.loc[prop]['Sale Date']) == pd._libs.tslibs.timestamps.Timestamp):
                    if(date >= indf1.loc[prop]['Sale Date'] and
                    type(outdf.loc[date][prop]) == float):
                        # print("Single Entry not in outdf")
                        outdf[prop][date] = indf1.loc[prop]['Loan Amount (MM)']

                elif(type(indf1.loc[prop]['Sale Date']) == pd.core.series.Series):
                    for i in range(0, len(indf1.loc[prop]['Sale Date'])):
                        if(type(indf1.loc[prop]['Sale Date'][i]) != float and
                        date >= indf1.loc[prop]['Sale Date'][i] and
                        type(outdf.loc[date][prop]) == float):
                            # print("Series Entry not in outdf ", i)
                            outdf[prop][date] = indf1.loc[prop]['Loan Amount (MM)'][i]

        # # Loans Dataset
        # for date in dates:
            print("ExtractLoans Loans: ", date)
            # For every timestep
            for prop in ids2:
                # For each property
                if(type(indf2.loc[prop]['Associated Sale Date']) == pd._libs.tslibs.timestamps.Timestamp):
                    if(date >= indf2.loc[prop]['Associated Sale Date'] and
                    type(outdf.loc[date][prop]) == float):
                        # print("Single Entry not in outdf")
                        outdf[prop][date] = indf2.loc[prop]['Loan Amount (MM)']

                elif(type(indf2.loc[prop]['Associated Sale Date']) == pd.core.series.Series):
                    for i in range(0, len(indf2.loc[prop]['Associated Sale Date'])):
                        if(type(indf2.loc[prop]['Associated Sale Date'][i]) != float and
                        date >= indf2.loc[prop]['Associated Sale Date'][i] and
                        type(outdf.loc[date][prop]) == float):
                            # print("Series Entry not in outdf ", i)
                            outdf[prop][date] = indf2.loc[prop]['Loan Amount (MM)'][i]
        return()

    def extract_rate_duration(dates, ids, indf, outdf1, outdf2):
        for date in dates:
            print('ExtractRateDuration : ', date)
            for prop in ids:
                if(type(indf.loc[prop]['Associated Sale Date']) == pd._libs.tslibs.timestamps.Timestamp):
                    if(date >= indf.loc[prop]['Associated Sale Date'] and
                    outdf1[prop][date] != outdf1[prop][date] and
                    outdf2[prop][date] != outdf2[prop][date]):
                        # print(indf.loc[prop]['Interest Rate %'])
                        outdf1[prop][date] = indf.loc[prop]['Interest Rate %']
                        # print(indf.loc[prop]['Loan Duration'])
                        outdf2[prop][date] = indf.loc[prop]['Loan Duration']


                elif(type(indf.loc[prop]['Associated Sale Date']) == pd.core.series):
                    for i in range(0, len(indf.loc[prop]['Associated Sale Date'])):
                        if(type(indf.loc[prop]['Associated Sale Date'][i]) != float and
                        date >= indf.loc[prop]['Associated Sale Date'][i] and
                        outdf1[prop][date] != outdf1[date][prop] and
                        outdf2[prop][date] != outdf2[date][prop]):
                            # print(indf.loc[prop]['Interest Rate %'][i])
                            outdf1[prop][date] = indf.loc[prop]['Interest Rate %'][i]
                            # print(indf.loc[prop]['Loan Duration'][i])
                            outdf2[prop][date] = indf.loc[prop]['Loan Duration'][i]
        return()

    # Fix time format from mm/dd/yyyy to yyyy-mm-dd
    def fixTimeFormat(fpath):
        filein = pd.read_csv(fpath, index_col=0)
        dates = []
        index = filein.index
        if(index[0] == '1/1/1950'):
            for i in index:
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
