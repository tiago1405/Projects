# Calculate mean price of acre in market/submaret as indicator of growth/valuation
# in area
# Fetch zillow data to use in each timestep as an estimate for property value
'''
Version: 1.0.2
Date: 18/03/2020
Author: Tiago Zanaga Da Costa

Real Estate modeling formulas for use in inferring data and creating features
from property, loan, sale, and rent and occupancy data of properties.

'''
import math as m

class Model_Formulas :

    # Property Sale CSV
    def month_of_ownership(curr_owner, prev_owner, curr_m_o_o):
        if(curr_owner == prev_owner):
            return (curr_m_o_o + 1)
        else:
            return 0

    # Property Loan and Property Sale CSVs
    def loan_to_value(sale_price, loan_value):

        return (loan_value/sale_price)*100

    # Property Data and Occupancy and Rent CSVs
    def egr(unit_count,avg_rent, occupancy_rate):

        return (unit_count*avg_rent)*(occupancy_rate/100)

    # Local Variable(s)  (EGR)
    def egr_growth(prev_egr, curr_egr):

        return ((curr_egr-prev_egr)/prev_egr)

    # Local Variable(s) (EGR)
    def opex(egr, exp_per):

        return (egr*exp_per)

    # Local Variable(s) (EGR)
    def noi(egr, opex_per_egr):

        return (egr-(egr*opex_per_egr))

    # Local Variable(s) (NOI) and Property Sale CSV
    def cap_rate(noi, sale_price):

        return (noi/sale_price)

    # Local Variable(s) (NOI)
    def capex_reserve(noi):

        return (noi*0.03)

    # Cashflow Before Debt Servicing
    # Local Variable(s) (NOI, Capex Reserve)
    def cbds(noi, capex_reserve):

        return (noi - capex_reserve)

    # Property Sale CSV
    def sale_proceeds(new_sale_price):

        return (new_sale_price*1000000)

    # Property Sale CSV
    def closing_costs(sale_price):

        return ((sale_price * 1000000) * -0.03)

    # Local Variable(s) (from: sale_proceeds)
    def cost_of_sale(sale_proceeds):

        return(sale_proceeds*-0.015)

    # Unlevered Net Cash Flow
    # Local Variable(s) (CBDS, Historical CBDS)
    def unl_ncf(curr_cbds, prev_cbds):

        return (curr_cbds + prev_cbds)

    # Property Loans CSV
    def loan_proceeds(loan_ammount):

        return (loan_ammount * 1000000)

    # Principal Payment per Month Timestep
    # Property Sale, Property Loan CSVs, and Local Variable(s) (m_o_o)
    def ppmt(m_o_o, curr_loan_val, loan_duration, interest_rate):

        # Interest Rate Per Period
        irpp = interest_rate / 12
        # Loan Duration in Months
        ldm = loan_duration * 12
        curr_loan_val = curr_loan_val * 1000000

        prin_pay = ((irpp*curr_loan_val) / (1 - (m.pow(1 + irpp, -(ldm)))))

        return(prin_pay)

    # Interest Payment per Month Timestep
    # Property Loan CSV
    def ipmt(interest_rate, loan_duration, curr_loan_val):

        return((interest_rate/12)*curr_loan_val)

    # Local Variable(s) (curr_total, curr_prin_pay)
    def loan_payoff(curr_total, curr_prin_pay):

        return(-(curr_total + curr_prin_pay))

    # Levered Net Cash Flow
    # Local Variable(s) (unl_ncf, prin_pay, int_pay, loan_payoff)
    def lncf(unl_ncf, prin_pay, int_pay, loan_payof):

        return(unl_ncf + prin_pay + int_pay + loan_payof)

    # Equity Position as a Percentage
    # Property Loan, Property Sale CSVs, and Local Variable(s) (prin_pay)
    def epp(loan_ammount, prin_pay, sale_price):

        return(1 - (((loan_ammount*1000000) + prin_pay) / (sale_price*1000000)))

    # Unlevered Expected Cash on Cash
    # Proprty Sale CSV, and Local Variable(s) (cbds)
    def uecoc(cbds, sale_price):
        if (sale_price == 0 or cbds == 0):
            return 0
        else:
            return(cbds / sale_price)

    # Levered Expected Cash on Cash
    # Local Variable(s) (cbds, prin_pay, int_pay, ltv)
    def lecoc(cbds, prin_pay, int_pay, ltv, sale_price):

        equity = (1-ltv)*sale_price

        cashflow = cbds - prin_pay - int_pay

        return(cashflow/equity)

    
