# Code by: Emily Costa

import numpy as np
import pandas as pd
import os

loan_path = os.path.join(os.path.expanduser('~'),'Documents',
            'saffron_capital','data_resources','samples','loans_sample.csv')
# print(loan_path)
prop_path = os.path.join(os.path.expanduser('~'),'Documents',
            'saffron_capital','data_resources','samples','property_data_sample.csv')
# print(prop_path)

loan_df = pd.read_csv(loan_path)
prop_df = pd.read_csv(prop_path)

# make dataframe of property ID along with classifying traits 
# (in this case, address only)
propID_df = pd.DataFrame(prop_df, columns=['PROPERTY_ID', 'PROPERTY_ADDRESS'])

# sort prior to matching to make it faster
# sorted_loan = loan_df.sort_values(by=['Address'])
# sorted_propID = propID_df.sort_values(by=['PROPERTY_ADDRESS'])

# property_IDs = dict(zip(propID_df.PROPERTY_ID, propID_df.PROPERTY_ADDRESS))

property_IDs = pd.merge(loan_df, prop_df, left_on='Address', right_on='PROPERTY_ADDRESS')

# key is ID, value is address
#for row in propID_df:
#    property_IDs[row['PROPERTY_ID']] = propID_df['PROPERTY_ADDRESS']

# loan_df['Property ID'] = property_IDs

property_IDs.to_csv('fixed_sample_data.csv')