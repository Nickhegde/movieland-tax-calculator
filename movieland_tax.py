import csv;
import json
import argparse
import math
from datetime import datetime;
from pathlib import Path;


#global declarations
unique_panels = set()
total_panel_count = 0
tax_bracket_2024 = []
income_data = []
taxable_income = 0
total_tax = 0
breakdown = []
green_bonus = 0
top_bracket = 0

def get_total_panel_count(file_path):
    with open(file_path, encoding='utf-8-sig', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) < 2:
                print(f"Warning: Skipping malformed row(expected at least 2 columns): {row}")
                continue            
            
            panel_id, date_str = row[0].strip(), row[1].strip()

            if not panel_id or not date_str:
                print(f"Warning: Skipping incomplete row : {row}")
                continue

            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                if date_obj.year == 2024:
                    unique_panels.add(panel_id)
            except ValueError:
                    print(f"Warning: Skipping row with Invalid date format : '{date_str}' (expected YYYY-MM-DD)")
                    continue
    return


#taxbracket_2024 = ceil((2023 taxbracket * 1.021) -37)
def generate_tax_brackets_2024(tax_bracket_2023):
    tax_bracket_2024 = []
    for bracket in tax_bracket_2023:
        new_bracket = {
            "Bracket": bracket["Bracket"],
            "Rate": bracket["Rate"],
            "UpperBound": math.ceil((bracket["UpperBound"] * 1.021) - 37) if bracket["UpperBound"] != float('inf') else float('inf')
        }
        tax_bracket_2024.append(new_bracket)
    return tax_bracket_2024


def read_income_data(file_path):
    with open(file_path, encoding='utf-8-sig', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) < 2:
                print(f"Warning: Skipping malformed row (expected 2 columns): {row}")
                continue
            
            month, gross_income = row[0].strip(), row[1].strip()

            if not month or not gross_income:
                print(f"Warning: Skipping row with missing fields: {row}")
                continue

            if not gross_income.replace(',', '').replace('.', '', 1).isdigit():
                    print(f"Warning: Skipping row with Invalid income value: '{gross_income}'")
                    continue

            try:
                month_obj = datetime.strptime(month, "%Y-%m")
            except ValueError:
                print(f"Warning: Skipping row with Invalid date format: '{month}' (expected YYYY-MM)")
                continue

            if month_obj.year == 2024:
                    income = float(gross_income.replace(",", ""))
                    income_data.append({
                        "Month": month_obj.month,
                        "GrossIncome": income
                    })


def generate_breakdown(bracket_value, taxable_value, rate_value, tax_value):
    global breakdown
    breakdown.append({
                "bracket": bracket_value,
                "taxable": taxable_value,
                "rate": rate_value,
                "tax": tax_value
            })

def get_round_tax(tax):
    tax = math.ceil(tax / 0.07) * 0.07
    return round(tax, 2)

def calculate_tax_for_year(month):
    global total_tax
    global taxable_income
    global breakdown
    global green_bonus
    total_tax = 0
    taxable_income = taxable_income + sum(income["GrossIncome"] for income in income_data[month:])
    breakdown = []

    if taxable_income >= 90000:
        green_bonus = 0


    tax = 0
    current_income = taxable_income
    for index, bracket in enumerate(tax_bracket_2024):
        if(index<len(tax_bracket_2024)-1):
            previous_bracket = tax_bracket_2024[index-1]["UpperBound"] if index > 0 else 0
            effective_bracket = bracket["UpperBound"] - previous_bracket
            current_bracket_tax = (effective_bracket * bracket["Rate"]) / 100
            tax += get_round_tax(current_bracket_tax)
            current_income = taxable_income - bracket["UpperBound"]
            generate_breakdown(bracket["Bracket"], effective_bracket, bracket["Rate"]/100, current_bracket_tax)
           
        else:
            current_bracket_tax = (current_income * bracket["Rate"]) / 100
            tax += get_round_tax(current_bracket_tax)
            generate_breakdown(bracket["Bracket"], current_income, bracket["Rate"]/100, current_bracket_tax)
            break
    
    total_tax = get_round_tax(tax)
    return


def calculate_tax_for_each_month():
    global total_tax
    global taxable_income
    global breakdown

    for income in income_data:
        month = income["Month"]
        gross_income = income["GrossIncome"]
        taxable_income = taxable_income + gross_income

        if taxable_income > top_bracket:
            calculate_tax_for_year(month)
            break
        else:
            tax = 0
            breakdown = []
            current_total_income = taxable_income
            for index,bracket in enumerate(tax_bracket_2024):
                if taxable_income <= bracket["UpperBound"]:
                    current_bracket_tax = (current_total_income * bracket["Rate"]) / 100
                    generate_breakdown(bracket["Bracket"], current_total_income, bracket["Rate"]/100, current_bracket_tax)
                    tax += get_round_tax(current_bracket_tax)
                    break
                else:
                    previous_bracket = tax_bracket_2024[index-1]["UpperBound"] if index > 0 else 0
                    effective_bracket = bracket["UpperBound"] - previous_bracket
                    current_bracket_tax = (effective_bracket * bracket["Rate"]) / 100   
                    tax += current_bracket_tax
                    generate_breakdown(bracket["Bracket"], effective_bracket, bracket["Rate"]/100, current_bracket_tax)
                    current_total_income = taxable_income - bracket["UpperBound"]
            total_tax = tax
            total_tax = get_round_tax(total_tax)
    return 



def calculate_final_tax_summary( taxable_income, total_tax, breakdown, basic, green_bonus):
    return {
        "taxable_income": taxable_income,
        "total_tax": total_tax,
        "effective_rate": round((total_tax / taxable_income if taxable_income > 0 else 0),2),
        "marginal_rate": breakdown[-1]["rate"] if breakdown else [],
        "breakdown": breakdown,
        "credits": {
            "basic": basic,
            "green_bonus": green_bonus,
            "net_tax": get_round_tax(total_tax - basic - green_bonus)
        }
    }



def main(args):
    global unique_panels, total_panel_count, tax_bracket_2024, income_data, taxable_income, total_tax, breakdown
    global green_bonus, top_bracket
    basic = 600

    incomePath = args.income_csv
    panelPath = args.panels_csv

        
    print(f"Income CSV Path: {incomePath}")
    print(f"Panels CSV Path: {panelPath}")

    get_total_panel_count(panelPath)
    total_panel_count = len(unique_panels)
    print(f"Total unique panels in 2024: {total_panel_count}")
    
    # tax brackets for 2024 calculation
    tax_bracket_2023= [
        {
            "Bracket": 1,
            "Rate": 7,
            "UpperBound": 2375
        },
        {
            "Bracket": 2,
            "Rate": 11,
            "UpperBound": 8950
        },
        {
            "Bracket": 3,
            "Rate": 16,
            "UpperBound": 23400
        },
        {
            "Bracket": 4,
            "Rate": 22,
            "UpperBound": 55800
        },
        {
            "Bracket": 5,
            "Rate": 29,
            "UpperBound": float('inf')  # No upper limit for the last bracket
        }
    ]
    tax_bracket_2024 = generate_tax_brackets_2024(tax_bracket_2023)
    print(f"Tax Brackets for 2024: {tax_bracket_2024}")

    #reading income data and format it
    read_income_data(incomePath)
    income_data.sort(key=lambda x: x["Month"])
    print(f"Income Data for 2024: {income_data}")

    # Calculate tax for each month
    green_bonus = 50 * total_panel_count if total_panel_count <20 else 20
    top_bracket = tax_bracket_2024[-2]["UpperBound"]

    calculate_tax_for_each_month()

    final_summary = calculate_final_tax_summary( taxable_income, total_tax, breakdown, basic, green_bonus)

    print(json.dumps(final_summary, indent=2))


class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print("Error: Please provide both 'income-csv' and 'panels-csv' file paths.")
        exit(1)


if __name__ == "__main__":
    parser = CustomArgumentParser(description="Process income and panel data.")
    parser.add_argument("income_csv", type=Path, help="Path to income.csv")
    parser.add_argument("panels_csv", type=Path, help="Path to panels.csv")
    args = parser.parse_args()
    main(args)