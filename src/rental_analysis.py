import numpy as np
import pandas as pd

class RentalAnalyzer:
    def __init__(self):
        # Convert ranges to numpy arrays for efficient operations
        self.rental_yield_ranges = {
            'Zone 1': np.array([0.028, 0.032, 0.036, 0.042]),  # 2.8% to 4.2%
            'Zone 2': np.array([0.033, 0.037, 0.042, 0.048])   # 3.3% to 4.8%
        }
        
        self.annual_costs = {
            'maintenance': 0.01,
            'insurance': 0.002,
            'void_periods': 0.08,
            'management_fee': 0.10,
            'service_charges': 0.005
        }
        
        self.annual_appreciation_scenarios = np.array([0.02, 0.035, 0.05, 0.065])

    def calculate_rental_income(self, property_value, zone):
        """Vectorized rental income calculation."""
        yields = self.rental_yield_ranges[zone]
        return (property_value * yields / 12)  # Returns numpy array of monthly rents

    def calculate_loan_amortization(self, loan_amount, annual_rate, years):
        """Vectorized loan amortization calculation."""
        monthly_rate = annual_rate / 100 / 12
        num_payments = years * 12
        
        # Calculate monthly payment
        monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / \
                         ((1 + monthly_rate)**num_payments - 1)
        
        # Create payment schedule using numpy arrays
        periods = np.arange(years * 12) + 1
        interest_payments = loan_amount * monthly_rate * (1 + monthly_rate)**(periods - 1) / \
                          ((1 + monthly_rate)**num_payments - 1)
        principal_payments = monthly_payment - interest_payments
        
        # Reshape and sum by year
        principal_by_year = principal_payments.reshape(-1, 12).sum(axis=1)
        interest_by_year = interest_payments.reshape(-1, 12).sum(axis=1)
        
        return principal_by_year, interest_by_year

    def calculate_cash_roi(self, property_value, deposit, monthly_mortgage, zone):
        """Calculate cash ROI for all rental yield scenarios."""
        monthly_rents = self.calculate_rental_income(property_value, zone)
        
        annual_property_costs = (
            property_value * self.annual_costs['maintenance'] +
            property_value * self.annual_costs['insurance'] +
            property_value * self.annual_costs['service_charges']
        )
        
        annual_rents = monthly_rents * 12
        void_costs = annual_rents * self.annual_costs['void_periods']
        management_costs = annual_rents * self.annual_costs['management_fee']
        
        total_annual_costs = (
            annual_property_costs +
            void_costs +
            management_costs +
            (monthly_mortgage * 12)
        )
        
        net_annual_income = annual_rents - total_annual_costs
        cash_roi = (net_annual_income / deposit) * 100
        
        return pd.DataFrame({
            'Monthly Rent': monthly_rents,
            'Annual Rent': annual_rents,
            'Total Costs': total_annual_costs,
            'Net Income': net_annual_income,
            'Cash ROI': cash_roi,
            'Rental Yield': (annual_rents / property_value) * 100
        })

    def calculate_total_roi(self, property_value, deposit, loan_amount, annual_rate, 
                          years, zone, analysis_period=5):
        """Calculate total ROI using numpy for efficient calculations across all scenarios."""
        monthly_payment = loan_amount * (annual_rate/100/12 * (1 + annual_rate/100/12)**(years*12)) / \
                         ((1 + annual_rate/100/12)**(years*12) - 1)
        
        monthly_rents = self.calculate_rental_income(property_value, zone)
        
        yearly_principal, yearly_interest = self.calculate_loan_amortization(
            loan_amount, annual_rate, analysis_period)
        cumulative_principal_paid = yearly_principal.sum()
        
        rents_grid, appreciation_grid = np.meshgrid(
            monthly_rents, 
            self.annual_appreciation_scenarios,
            indexing='ij'
        )
        
        annual_rents = rents_grid * 12
        
        annual_property_costs = (
            property_value * self.annual_costs['maintenance'] +
            property_value * self.annual_costs['insurance'] +
            property_value * self.annual_costs['service_charges']
        )
        
        void_costs = annual_rents * self.annual_costs['void_periods']
        management_costs = annual_rents * self.annual_costs['management_fee']
        total_annual_costs = (
            annual_property_costs +
            void_costs +
            management_costs +
            (monthly_payment * 12)
        )
        
        net_annual_income = annual_rents - total_annual_costs
        cumulative_cash_flow = net_annual_income * analysis_period
        
        final_property_values = property_value * (1 + appreciation_grid)**analysis_period
        total_appreciation = final_property_values - property_value
        
        total_returns = (
            cumulative_cash_flow +
            cumulative_principal_paid +
            total_appreciation
        )
        
        annualized_roi = ((1 + total_returns/deposit)**(1/analysis_period) - 1) * 100
        cash_roi = (net_annual_income / deposit) * 100
        rental_yields = (annual_rents / property_value) * 100
        
        scenarios = []
        for i in range(len(monthly_rents)):
            for j in range(len(self.annual_appreciation_scenarios)):
                scenarios.append({
                    'Monthly Rent': monthly_rents[i],
                    'Appreciation Rate': self.annual_appreciation_scenarios[j] * 100,
                    'Cash Flow': cumulative_cash_flow[i,j],
                    'Principal Paid': cumulative_principal_paid,
                    'Appreciation': total_appreciation[i,j],
                    'Total Return': total_returns[i,j],
                    'Annualized Total ROI': annualized_roi[i,j],
                    'Cash ROI': cash_roi[i,j],
                    'Final Property Value': final_property_values[i,j],
                    'Rental Yield': rental_yields[i,j]
                })
        
        return pd.DataFrame(scenarios)
