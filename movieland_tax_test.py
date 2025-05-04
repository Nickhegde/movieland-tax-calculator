import unittest
import math
import movieland_tax 

class TestMovieLandTax(unittest.TestCase):

    def test_generate_tax_brackets_2024(self):
        tax_bracket_2023 = [
            {"Bracket": 1, "Rate": 7, "UpperBound": 2375},
            {"Bracket": 2, "Rate": 11, "UpperBound": 8950},
            {"Bracket": 3, "Rate": 16, "UpperBound": 23400},
            {"Bracket": 4, "Rate": 22, "UpperBound": 55800},
            {"Bracket": 5, "Rate": 29, "UpperBound": float('inf')}
        ]
        expected_upper_bounds = [
           2388, 9101, 23855, 56935, float('inf')
        ]
        result = movieland_tax.generate_tax_brackets_2024(tax_bracket_2023)
        for i, bracket in enumerate(result):
            self.assertEqual(bracket["UpperBound"], expected_upper_bounds[i])

    def setUp(self):
        # Set up the test environment before each test
        movieland_tax.tax_bracket_2024 = [
            {"Bracket": 1, "Rate": 10, "UpperBound": 1000},
            {"Bracket": 2, "Rate": 20, "UpperBound": 3000},
            {"Bracket": 3, "Rate": 30, "UpperBound": float('inf')}
        ]
        movieland_tax.income_data = [
            {"Month": 1, "GrossIncome": 500},
            {"Month": 2, "GrossIncome": 1000}
        ]
        movieland_tax.top_bracket = 3000 
        movieland_tax.total_tax = 0
        movieland_tax.taxable_income = 0
        movieland_tax.breakdown = []

    def test_calculate_tax_for_each_month(self):
        movieland_tax.calculate_tax_for_each_month()
        # Check the expected side effects
        self.assertGreater(movieland_tax.total_tax, 0)
        self.assertEqual(movieland_tax.taxable_income, 1500)
        self.assertTrue(len(movieland_tax.breakdown) > 0)
        self.assertIn("bracket", movieland_tax.breakdown[0])

    def test_calculate_final_tax_summary(self):
        taxable_income = 100000
        total_tax = 20000
        breakdown = [{"bracket": 5, "taxable": 100000, "rate": 0.2, "tax": 20000}]
        basic = 600
        green_bonus = 1000

        summary = movieland_tax.calculate_final_tax_summary(taxable_income, total_tax, breakdown, basic, green_bonus)
        
        self.assertEqual(summary["taxable_income"], 100000)
        self.assertEqual(summary["total_tax"], 20000)
        self.assertEqual(summary["credits"]["net_tax"], 18400)

if __name__ == '__main__':
    unittest.main()
