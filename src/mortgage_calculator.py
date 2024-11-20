import numpy as np
import pandas as pd

class MortgageCalculator:
    def __init__(self):
        # UK mortgage rates for London properties (Q1 2024)
        # Ranges based on compilation of rates from major UK lenders
        # Including: Nationwide, Barclays, HSBC, NatWest, Santander
        # Format: LTV: [lowest_rate, lower_mid_rate, higher_mid_rate, highest_rate]
        self.base_rates = {
            95: [5.89, 6.34, 6.79, 7.15],    # 95% LTV
            90: [5.49, 5.89, 6.29, 6.69],    # 90% LTV
            85: [5.19, 5.54, 5.89, 6.29],    # 85% LTV
            80: [4.89, 5.24, 5.59, 5.99],    # 80% LTV
            75: [4.59, 4.94, 5.29, 5.69],    # 75% LTV
            70: [4.39, 4.74, 5.09, 5.49],    # 70% LTV
            65: [4.29, 4.64, 4.99, 5.39],    # 65% LTV
            60: [4.19, 4.54, 4.89, 5.29]     # 60% LTV
        }
        
        # Additional factors that can affect rates
        self.rate_adjustments = {
            'new_build': 0.2,          # New build premium
            'buy_to_let': 0.5,         # Buy-to-let premium
            'high_value': -0.2,        # Discount for loans > £1M
            'professional': -0.15       # Professional mortgage discount
        }
    
    def calculate_monthly_payment(self, principal, annual_rate, years):
        """Calculate monthly mortgage payment."""
        monthly_rate = annual_rate / 100 / 12
        num_payments = years * 12
        
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate)**num_payments) / \
                         ((1 + monthly_rate)**num_payments - 1)
        
        return monthly_payment
    
    def get_required_deposit(self, property_value, ltv):
        """Calculate required deposit based on LTV."""
        return property_value * (1 - ltv/100)
    
    def get_rate_for_ltv(self, ltv):
        """Get the approximate interest rate based on LTV."""
        for threshold, rate_range in sorted(self.base_rates.items()):
            if ltv <= threshold:
                return rate_range
        return max(self.base_rates.values())
    
    def analyze_scenarios(self, property_value, years=25):
        """Analyze different LTV scenarios with multiple rate points."""
        scenarios = []
        
        for ltv in sorted(self.base_rates.keys()):
            deposit = self.get_required_deposit(property_value, ltv)
            loan_amount = property_value - deposit
            rates = self.base_rates[ltv]  # Now gets all 4 rates
            
            # Calculate monthly payments for each rate
            monthly_payments = [
                self.calculate_monthly_payment(loan_amount, rate, years)
                for rate in rates
            ]
            
            scenarios.append({
                'LTV': ltv,
                'Deposit': deposit,
                'Loan Amount': loan_amount,
                'Best Rate': rates[0],
                'Lower Mid Rate': rates[1],
                'Higher Mid Rate': rates[2],
                'Worst Rate': rates[3],
                'Best Monthly': monthly_payments[0],
                'Lower Mid Monthly': monthly_payments[1],
                'Higher Mid Monthly': monthly_payments[2],
                'Worst Monthly': monthly_payments[3]
            })
        
        return pd.DataFrame(scenarios)
