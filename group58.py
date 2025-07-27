import json
import os
import datetime
import math
import re


company_name = input("Input Company Name: ")
analyst_name = input("Input Analyst Name: ")
date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
fixed_cost = int(input("Input Total Fixed Cost: "))
variable_cost_per_unit = int(input("Input Variable Cost Per Unit: "))
selling_price_per_unit = int(input("Selling Price per Unit: "))
units_sold = int(input("Units Sold: "))
total_expenses = int(input("Total Expenses: "))
investment_cost = int(input("Investment Cost: "))
annual_cash_inflow = int(input("Annual Cash Inflow: "))
safe_name = re.sub(r'\W+', '_', company_name.lower()+date.lower())
os.makedirs("reports", exist_ok=True)
safe_path = os.path.join("reports", safe_name)

class allAnalyse:
    def __init__(self, fc, vcpu, sppu, us, ic, aci,cn,an, date, sn, te=0,):
        self.fc = fc
        self.vcpu = vcpu
        self.sppu = sppu
        self.us = us
        self.te = te
        self.ic = ic
        self.aci = aci
        self.cn = cn
        self.an = an
        self.date = date
        self.filename = sn + ".txt"

    
    def calculate_break_even_analyser(self):
        # Break Even Unit = Fixed Cost / Simple Price Per Unit - Input Variable Cost Per Unit
        BEU = self.fc/(self.sppu-self.vcpu)
        # Contribution Margin Ratio = Simple Price Per Unit - Input Variable Cost Per Unit / Selling Price
        CMR = (self.sppu-self.vcpu)/self.sppu
        BER = self.fc/CMR

        result =  {
            "Break Even Unit (for products)": BEU,
            "Break-Even Revenue (for services or bundles)": BER
        }
        with open(self.filename, "a") as f:
            f.write("\nBREAK EVEN ANALYSIS REPORT")
            f.write("-" * 40)
            for key, value in result.items():
                f.write(f"\n{key:<30}: {value:.2f}\n")
        


    def calculate_profit(self):
        profit = (self.sppu - self.vcpu) * self.us - self.fc
        
        
        return profit

    def analyse_pricing(self):
        """CM per Unit = Selling Price per Unit - Variable Cost per Unit
        CM Ratio = CM per Unit / Selling Price per Unit
        Break-Even Units = Fixed Costs / CM per Unit
        Break-Even Revenue = Fixed Costs / CM Ratio
        Units for Target Profit = (Fixed Costs + Target Profit) / CM per Unit
        Markup % = (Selling Price - Cost) / Cost × 100
        Gross Profit = Revenue - Cost of Goods Sold
        GPM = Gross Profit / Revenue × 100
        NPM = Net Profit / Revenue × 100
        PED = % Change in Quantity Demanded / % Change in Price
        Profit per Unit = Selling Price - Variable Cost - Fixed Cost per Unit
        Fixed Costs, Variable Cost per Unit, Selling Price per Unit, Contribution Margin, Break-Even Point, Profit at Given Sales Volume, Profit Margins
        """
        revenue = self.sppu * self.us
        cm = self.sppu-self.vcpu
        BEU = self.fc/(self.sppu-self.vcpu)
        pagsv = (self.us * cm) - self.fc
        gpm = ((revenue - (self.vcpu * self.us)) / revenue) * 100
        npm = ((pagsv - self.te) / revenue) * 100
        price_analysis = {
        "Revenue": round(revenue, 2),
        "Contribution Margin per Unit": round(cm, 2),
        "Break-Even Units": round(BEU, 2),
        "Profit at Given Sales": round(pagsv, 2),
        "Gross Profit Margin (%)": round(gpm, 2),
        "Net Profit Margin (%)": round(npm, 2)
    }
        with open(self.filename, "a") as f:
            f.write("\nPRICE ANALYSIS REPORT")
            f.write("-" * 40)
            for key, value in price_analysis.items():
                f.write(f"\n{key:<30}: {value:.2f}\n")
        

    def calculate_investment(self):
        """Investment Analysis: Return on Investment (ROI) = (Net Profit / Investment Cost) * 100
        Average Cost of Investment = Total Expenses / Investment Cost
        """
        net_profit = self.calculate_profit() - self.te
        roi = (net_profit / self.ic) * 100
        payback_period = math.ceil(self.ic / self.aci)
        investment_analysis = {
            "Return on Investment (%)": round(roi, 2),
            "Payback Period": round(payback_period, 2)
        }
        with open(self.filename, "a") as f:
            f.write("\nINVESTMENT ANALYSIS REPORT")
            f.write("-" * 40)
            for key, value in investment_analysis.items():
                f.write(f"\n{key}: {value:.2f}")

    def sensitivity_analysis(self):
        results = []

        # Vary selling price (+/- 10%, 20%)
        for change in [-0.2, -0.1, 0.1, 0.2]:
            new_price = self.sppu * (1 + change)
            profit = self.calculate_profit()
            results.append((f"Price {int(change*100):+}%", new_price, profit))
            # print(f"Price {int(change*100):+}%       | {new_price:.2f}     | {profit:.2f}")

        # Vary variable cost (+/- 10%, 20%)
        for change in [-0.2, -0.1, 0.1, 0.2]:
            new_vcost = self.vcpu * (1 + change)
            profit = self.calculate_profit()
            results.append((f"Cost {int(change*100):+}%", new_vcost, profit))
            # print(f"Cost {int(change*100):+}%        | {new_vcost:.2f}     | {profit:.2f}")
        
        # Vary units sold (+/- 10%, 20%)
        for change in [-0.2, -0.1, 0.1, 0.2]:
            new_units = int(self.us * (1 + change))
            profit = self.calculate_profit()
            results.append((f"Units {int(change*100):+}%", new_units, profit))
            # print(f"Units {int(change*100):+}%       | {new_units}       | {profit:.2f}")

        return results
    def calculate_profit_metrics(self):
        revenue = self.sppu * self.us
        variable_cost = self.vcpu * self.us
        total_cost = self.fc + variable_cost
        profit = revenue - total_cost
        margin = (profit / revenue) * 100 if revenue != 0 else 0
        break_even_units = self.fc / (self.sppu - self.vcpu) if self.sppu != self.vcpu else float('inf')
        return {
            "Revenue": revenue,
            "Variable Cost": variable_cost,
            "Total Cost": total_cost,
            "Profit": profit,
            "Profit Margin (%)": margin,
            "Break-Even Units": break_even_units
        }
    def generate_recommendations(self):
        recs = []
        if self.calculate_profit_metrics()["Profit Margin (%)"] < 20:
            recs.append("Consider increasing price to improve margins.")
        if self.calculate_profit_metrics()["Break-Even Units"] > 1000:
            recs.append("High break-even: Consider reducing fixed or variable costs.")
        for label, val, profit in self.sensitivity_analysis():
            if "Price +10%" in label and profit > self.calculate_profit_metrics()["Profit"]:
                recs.append("Increasing price by 10% may increase profit.")
            if "Cost -10%" in label and profit > self.calculate_profit_metrics()["Profit"]:
                recs.append("Reducing unit cost by 10% may improve profitability.")
            if "Volume +10%" in label and profit > self.calculate_profit_metrics()["Profit"]:
                recs.append("Increasing sales volume can improve profit.")
        return recs or ["\nNo strong recommendations, try running with new values."]
    def print_report(self):
        with open(self.filename, "a") as f:
            f.write("\nPROFITABILITY REPORT")
            f.write("-" * 40)
            for k, v in self.calculate_profit_metrics().items():
                f.write(f"\n{k:<20}: {v:.2f}")
            f.write("\n\nSENSITIVITY ANALYSIS")
            f.write("-" * 40)   
            for label, val, profit in self.sensitivity_analysis():
                f.write(f"\n{label:<15} | {val:<7} | Profit: {profit:.2f}")
            f.write("\n\nRECOMMENDATIONS")
            f.write("-" * 40)
            for r in self.generate_recommendations():
                f.write(r)
        


class codeRun(allAnalyse):
    def generate_report_file(self):
        json_metrics = {
            "company": self.cn,
            "analyst": self.an,
            "date": self.date,
            "revenue": self.calculate_profit_metrics()["Revenue"],
            "profit": self.calculate_profit_metrics()["Profit"],
            "recommendations": self.generate_recommendations()
        }
        json_filename = self.filename.replace(".txt", ".json")
        with open(json_filename, "w") as jf:
            json.dump(json_metrics, jf, indent=4)

        print(f"JSON report generated: {json_filename}")
        with open(self.filename, "w") as f:
            f.write(f"CSC202 PROJECT FOR GROUP 58\n")
            f.write(f"Generated on: {self.date}\n")
            f.write(f"Project Task: Break-Even Analyzer and Profitability Calculator Build a financial analysis tool that calculates break-even points for products and services, implements profitability analysis using fixed and variable costs, analyzes pricing strategies and margin optimization, calculates return on investment and payback periods, performs sensitivity analysis for different scenarios, and generates profitability reports with pricing recommendations and cost structure optimization.")
            f.write("-" * 40 + "\n")
            f.write(f"Report for {self.cn}\n")
            f.write(f"Analyst: {self.an}\n")

        self.calculate_break_even_analyser()

        self.analyse_pricing()
        self.calculate_investment()
        self.print_report()
        
        with open(self.filename, "a") as f:
            f.write(f"\n\n\nThe Profit at {self.us} unit sold is {self.calculate_profit()}")
        
        print(f"Report generated: {self.filename}")
    def runner(self):
        if self.sppu <= 0:
            raise ValueError("Selling Price Per Unit must be greater than 0.")

        if self.vcpu < 0:
            raise ValueError("Variable Cost Per Unit cannot be negative.")

        if self.vcpu >= self.sppu:
            raise ValueError("Variable Cost must be less than Selling Price.")

        if self.fc < 0:
            raise ValueError("Fixed Cost cannot be negative.")

        if self.us < 0:
            raise ValueError("Units Sold must be zero or more.")

        if self.te < 0:
            raise ValueError("Total Expenses (TE) cannot be negative.")

        if self.ic <= 0:
            raise ValueError("Initial Investment (IC) must be greater than 0.")

        if self.aci < 0:
            raise ValueError("Annual Cash Inflow (ACI) cannot be negative.")

        self.generate_report_file()
        

analysis = codeRun(fixed_cost, variable_cost_per_unit, selling_price_per_unit, units_sold,  investment_cost, annual_cash_inflow, company_name , analyst_name, date, safe_path, total_expenses)

analysis.runner()