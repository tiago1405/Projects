import pandas as pd
import numpy as np
import os as os
from model_formulas import Model_Formulas as mf
from FeatureSupportFunctions import FeatureSupportFunctions as fsf
from datetime import datetime as dt
import math as math
import pprint

class FeatureGenerationFunctions:
    '''
    Version: 1.1.0
    Date: 08/07/2020
    Author: Tiago Zanaga Da Costa

    Read in CSV file into a pandas data frame.
    csv_file_path   = file path to csv (i.e.: ./home/usr/documents/csv_file)
    csv_data        = pandas data frame generated from reading in CSV data
    '''

    '''
    #Function:
        FeatureGenerationFunctions.GenerateFeatures
    #Description:
        Read prepared CSVs into Pandas Data Frames and perform calculation on
    values to generate Model Features and output a time indexed Model for
    properties in a Real Estate Market.
    #Given Variables:
        ro_fps     = Array of File Paths for the Rent and Occupancy CSVs
        ro_fps     = [
            [0] or_fp       = Occupancy Rate CSV File Path
            [1] ra_fp       = Rent Actual CSV File Path
            [2] rm_fp       = Rent Market CSV File Path
            [3] rpsfa_fp    = Rent Per Square Feet Actual CSV File Path
            [4] rpsfm_fp    = Rent Per Square Feet Market CSV File Path
        ]
        aux_fps     = Array of File Paths for the Auxiliary Files
        aux_fps    = [
            [0] pd_fp       = Property Data CSV File Path
            [1] sa_fp       = Sales Amount CSV File Path
            [2] la_fp       = Loans Amoutn CSV File Path
            [3] ld_df       = Loans Duration CSV File Path
            [4] lr_df       = Loans Rates CSV File Path

        ]
        output_path = The path where to save the Model as a CSV
    #Output:
        A Model in CSV format for all properties in a real estate market.
    ''' '''

    '''
    def GenerateFeatures(ro_fps, aux_fps, output_path):

        dates = []
        unit_nums = []
        prop_ids = []
        gen_feat_ids = []
        feat_list = ["curr_loan_amount", "month_of_ownership", "LTV", "EGR",
        "egr_growth", "OPEX", "NOI", "cap_rate", "capex_reserves", "CBDS",
        "sale_proceeds", "closing_costs", "cost_of_sale", "UNCF", "loan_proceeds",
        "PPMT", "IPMT", "loan_payoff", "LNCF", "EPP", "UECOC", "LECOC"]
        counter = 0
        num_props = 0

        '''Read in Rent and Occupancy CSVs into pandas data frames
        df = [pandas] data frame                                '''
        or_df = pd.read_csv(ro_fps[0], index_col=0)
        ra_df = pd.read_csv(ro_fps[1], index_col=0)
        rm_df = pd.read_csv(ro_fps[2], index_col=0)
        rpsfa_df = pd.read_csv(ro_fps[3], index_col=0)
        rpsfm_df = pd.read_csv(ro_fps[4], index_col=0)
        '''Read in the Auxiliary (Property Data , Loans, and Sales)
        CSVs into pandas data frames'''
        # Index_col = Property_IDs
        pd_df = pd.read_csv(aux_fps[0], index_col=1)
        # Index_col = time (dates)
        sa_df = pd.read_csv(aux_fps[1], index_col=0)
        la_df = pd.read_csv(aux_fps[2], index_col=0)
        ld_df = pd.read_csv(aux_fps[3], index_col=0)
        lr_df = pd.read_csv(aux_fps[4], index_col=0)

        '''Sort the columns (and rows) (=property_id) in ascending order'''
        or_df = or_df.reindex(sorted(or_df.columns), axis=1)
        ra_df = ra_df.reindex(sorted(ra_df.columns), axis=1)
        rm_df = rm_df.reindex(sorted(rm_df.columns), axis=1)
        rpsfa_df = rpsfa_df.reindex(sorted(rpsfa_df.columns), axis=1)
        rpsfm_df = rpsfm_df.reindex(sorted(rpsfm_df.columns), axis=1)
        pd_df = pd_df.sort_values(by=['PROPERTY_ID'], ascending=True)

        '''Drop the First column (old index 0:prop_num)'''
        pd_df = pd_df.drop(['Unnamed: 0'], axis=1)

        '''Store the index of or_df (years) into a list to be used in the for loop'''
        for date in or_df.iterrows():
            dates.append(date[0])

        '''Find number of properties in this market'''
        num_props = len(or_df.loc[dates[0], :])

        '''Store number of units per Property and all property ids
        for the market into an array as well as adding property ids to
        generated features to be used in indexing'''
        for prop_n in range(0, num_props):
            unit_nums.append(pd_df.loc[or_df.columns[prop_n]]['PROPERTY_UNITS'])
            prop_ids.append(or_df.columns[prop_n])
            for i in range(0, len(feat_list)):
                gen_feat_ids.append(or_df.columns[prop_n] + "-" + feat_list[i])

        ''' Create the numpy arrays where we will store generated values which will
         be used in calculations for generating the features '''
        prev_egr = np.zeros(shape=(num_props), dtype=float)
        prev_cbds = np.zeros(shape=(num_props), dtype=float)
        owner_month = np.zeros(shape=(num_props), dtype=int)
        curr_loan_amount = np.zeros(shape=(num_props), dtype=float)
        curr_payoff = np.zeros(shape=(num_props), dtype=float)
        # Initialize prev_date as the first date
        prev_date = dates[0]


        # THE FINAL DATAFRAME CONTAINING THE MODEL WITH GENERARED FEATURES
        model = pd.DataFrame(index=dates, columns=gen_feat_ids)
        model_ind = ''
        '''
        ## print(index):
        Prints out the current year of the time series data being accessed

        ## unit_nums[prop_n]

        ## or_df.columns[prop_n] --> PROPERTY_ID

        ## pd_df.loc[or_df.columns[prop_n]] :
        Outputs the data for the row in PropertyData.csv that corresponds to the
        property_id of the current property being iterated through.
        Current Property (prop_n) --> OccupancyRate (or_df) Column Header (PROPERTY_ID)
        --> PropertyData (pd_df) --> Data on Current Property (Row of pd_df)

        ## or_df.loc[index, :][prop_n] :
        Outputs the Occupancy Rate data for each property at each year

        ## ra_df.loc[index, :][prop_n] :
        Outputs the Rent Actual data for each property at each year
        '''
        print()
        for date in dates:
            # print(date)
            for prop_n in range(0, num_props):
                # print("\nProerty Num: " + str(prop_n))
                prop_id = or_df.columns[prop_n]

                '''Calculate Current Loan Amount'''
                # print('curr_loan_amount')
                model_ind = prop_id+'-'+'curr_loan_amount'
                if(date == dates[0]):
                    curr_loan_amount[prop_n] = la_df[prop_id][date]
                elif(la_df[prop_id][date] != la_df[prop_id][prev_date]):
                    curr_loan_amount[prop_n] = la_df[prop_id][date]
                model[model_ind][date] = curr_loan_amount[prop_n]

                '''Calculate Month of Ownership'''
                # print('month_of_ownership')
                model_ind = prop_id+'-'+'month_of_ownership'
                if(prev_date != dates[0] and
                sa_df[prop_id][date] == sa_df[prop_id][prev_date]):
                    owner_month[prop_n] = owner_month[prop_n] + 1
                    # print("Month: ", owner_month[prop_n][counter])
                else:
                    owner_month[prop_n] = 0

                model[model_ind][date] = owner_month[prop_n]
                '''Calculate Loan to Value Ration (LTV)'''
                # print('ltv')
                model_ind = prop_id+'-'+'LTV'
                ltv = mf.loan_to_value(sa_df[prop_id][date], la_df[prop_id][date])
                # print(ltv)
                model[model_ind][date] = ltv
                '''Calculate Effective Gross Revenue (EGR)'''
                # print('egr')
                model_ind = prop_id+'-'+'EGR'
                egr = mf.egr(pd_df.loc[prop_id]['PROPERTY_UNITS'],
                ra_df.loc[date, :][prop_n], or_df.loc[date, :][prop_n])
                # print("EGR: " + str(egr))
                model[model_ind][date] = egr
                '''Calculate EGR Growth from previous month'''
                # print('egr_growth')
                model_ind = prop_id+'-'+'egr_growth'
                egr_growth = 0
                if(egr >= 0 or egr <= 0):
                    egr_growth = mf.egr_growth(prev_egr[prop_n], egr)
                    # egr_growth = (egr-prev_egr[prop_n])
                elif(egr == 0 or type(egr) == str):
                    egr_growth = 0
                # print("EGR Growth: " + str(egr_growth))
                model[model_ind][date] = egr_growth
                '''Calculate Operating Expenditures (OPEX)'''
                # print('opex')
                model_ind = prop_id+'-'+'OPEX'
                opex = mf.opex(egr)
                # print("OPEX: " + str(opex))
                model[model_ind][date] = opex
                '''Calculate Net Operating Income (NOI)'''
                # print('noi')
                model_ind = prop_id+'-'+'NOI'
                noi = mf.noi(egr, (opex/egr))
                # print("NOI: " + str(noi))
                model[model_ind][date] = noi

                '''Calculate Cap Rate'''
                model_ind = prop_id+'-'+'cap_rate'

                '''Calculate Capital Expenditure Reserves (CAPEX Reserves)'''
                # print('capex_res')
                model_ind = prop_id+'-'+'capex_reserves'
                capex_res = mf.capex_reserve(noi)
                # print("CAPEX Reserve: " + str(capex_res))
                model[model_ind][date] = capex_res
                '''Calculate Cashflow Before Debt Servicing (CBDS)'''
                # print('cbds')
                model_ind = prop_id+'-'+'CBDS'
                cbds = mf.cbds(noi, capex_res)
                prev_cbds[prop_n] = cbds
                # print("CBDS: " + str(cbds))
                model[model_ind][date] = cbds
                '''Calculate Sale Proceeds'''
                # print('sale_proceeds')
                model_ind = prop_id+'-'+'sale_proceeds'
                if(sa_df[prop_id][date] != sa_df[prop_id][prev_date]):
                    sale_p = mf.sale_proceeds(sa_df[prop_id][date])
                model[model_ind][date] = sale_p
                '''Calculate Closing Costs'''
                model_ind = prop_id+'-'+'closing_costs'

                '''Calculate Cost of Sale'''
                model_ind = prop_id+'-'+'cost_of_sale'

                '''Calculate Unlevered Net Cash Flow'''
                # print('UNCF')
                model_ind = prop_id+'-'+'UNCF'
                # if(counter != 0):
                uncf = mf.unl_ncf(cbds, prev_cbds[prop_n])
                    # print("UNCF: " + str(uncf))
                model[model_ind][date] = uncf
                '''Calculate Loan Proceeds'''
                # print('loan_proceeds')
                model_ind = prop_id+'-'+'loan_proceeds'
                l_proc = mf.loan_proceeds(la_df[prop_id][date])
                model[model_ind][date] = l_proc
                '''Calculate Principal Payment per Month Timestep (PPMT)'''
                # print('PPMT')
                model_ind = prop_id+'-'+'PPMT'
                ppmt = mf.ppmt(owner_month[prop_n],
                curr_loan_amount[prop_n],
                ld_df[prop_id][date], lr_df[prop_id][date])
                model[model_ind][date] = ppmt
                '''Calculate Interest Payment per Month Timestep (IPMT)'''
                # print('IMPT')
                model_ind = prop_id+'-'+'IPMT'
                ipmt = mf.ipmt(lr_df[prop_id][date], ld_df[prop_id][date], curr_loan_amount[prop_n])
                model[model_ind][date] = ipmt
                '''Calculate Loan Payoff'''
                # print('loan_payof')
                model_ind = prop_id+'-'+'loan_payoff'
                lpo = mf.loan_payoff(curr_payoff[prop_n], ppmt)
                curr_payoff[prop_n] = -(lpo)
                model[model_ind][date] = lpo
                '''Calculate Levered Net Cash Flow'''
                # print('LNCF')
                model_ind = prop_id+'-'+'LNCF'
                lncf = mf.lncf(uncf, ppmt, ipmt, lpo)
                model[model_ind][date] = lncf
                '''Calculate Equity Position as a Percentage (EPP)'''
                # print('EPP')
                model_ind = prop_id+'-'+'EPP'
                epp = mf.epp(la_df[prop_id][date], ppmt, sa_df[prop_id][date])
                model[model_ind][date] = epp
                '''Calculate Unlevered Expected Cash on Cash'''
                # print('UECOC')
                model_ind = prop_id+'-'+'UECOC'
                uecoc = mf.uecoc(cbds, sa_df[prop_id][date])
                model[model_ind][date] = uecoc
                '''Calculate Levered Expected Cash on Cash'''
                # print('LECOC')
                model_ind = prop_id+'-'+'LECOC'
                lecoc = mf.lecoc(cbds, ppmt, ipmt, ltv, sa_df[prop_id][date])
                model[model_ind][date] = lecoc

                prev_egr[prop_n] = egr

            prev_date = date
            counter += 1

        model.to_csv(output_path, sep=',', encoding='utf8')
        return()

    def newDataGen(modelfp, marketDatafp, output_path):
        model_df = pd.read_csv(modelfp, index_col=0)
        mktd_df = pd.read_csv(marketDatafp, index_col=0)
        dates = mktd_df.index
        prop_ids = []
        headers = []

        # separate strings at '-' to get the property ID
        for column in model_df.columns:
            if "EGR" in column:
                headers.append(column)

        for date in dates:
            # Print date for first month of each year
            # if "-01-" in date:
                # print(date)
            for head in headers:
                header = head.split("-")
                prop_id = header[0]
                x = prop_id + '-OPEX'
                if ~np.isnan(mktd_df['Expenses %'][date]) and ~np.isnan(model_df[x][date]):
                    # model_df[x][date] = model_df[head][date] * mktd_df['Expenses %'][date]
                    model_df.loc[date, x] = model_df[head][date] * mktd_df['Expenses %'][date]
                else:
                    # model_df[x][date] = 0.0
                    model_df.loc[date, x] = 0.0

        model_df.to_csv(output_path, sep=',', encoding='utf-8')
        return()
