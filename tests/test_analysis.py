import pandas as pd
import unittest

from analysis import category_sales, monthly_sales, summary_metrics
from data_cleaning import clean_transactions
from data_loader import validate_columns


def sample_frame():
    return pd.DataFrame({
        "Order ID": ["A-1", "A-2", "A-3"],
        "Order Date": ["2024-01-05", "2024-01-20", "2024-02-02"],
        "Region": ["North", "North", "West"],
        "City": ["Delhi", "Delhi", "Pune"],
        "Customer Segment": ["Consumer", "Corporate", "Consumer"],
        "Category": ["Electronics", "Electronics", "Clothing"],
        "Sub-Category": ["Audio", "Audio", "Footwear"],
        "Quantity": [2, 1, 3],
        "Unit Price": [100.0, 200.0, 50.0],
        "Discount": [0.0, 0.1, 0.0],
        "Sales": [200.0, 180.0, 150.0],
        "Profit": [40.0, -10.0, 20.0],
        "Ship Mode": ["Standard", "Express", "Standard"],
    })


class RetailAnalysisTests(unittest.TestCase):
    def test_supplied_sales_and_profit_are_aggregated(self):
        clean, _ = clean_transactions(sample_frame())
        metrics = summary_metrics(clean)
        self.assertEqual(metrics["sales"], 530)
        self.assertEqual(metrics["profit"], 50)
        self.assertEqual(metrics["orders"], 3)
        self.assertEqual(metrics["quantity"], 6)

    def test_duplicate_removal(self):
        raw = pd.concat([sample_frame(), sample_frame().iloc[[0]]], ignore_index=True)
        clean, audit = clean_transactions(raw)
        self.assertEqual(audit["duplicate_rows_removed"], 1)
        self.assertEqual(len(clean), 3)

    def test_dates_and_monthly_aggregation(self):
        clean, _ = clean_transactions(sample_frame())
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(clean["Order Date"]))
        monthly = monthly_sales(clean)
        self.assertEqual(len(monthly), 2)
        self.assertEqual(monthly.iloc[0]["Sales"], 380)

    def test_negative_profit_is_valid(self):
        clean, audit = clean_transactions(sample_frame())
        self.assertTrue(clean["IsValid"].all())
        self.assertEqual(audit["negative_profit_rows"], 1)

    def test_category_aggregation(self):
        clean, _ = clean_transactions(sample_frame())
        result = category_sales(clean)
        self.assertEqual(result.iloc[0]["Category"], "Electronics")
        self.assertEqual(result.iloc[0]["Sales"], 380)

    def test_invalid_quantity_is_excluded(self):
        raw = sample_frame()
        raw.loc[0, "Quantity"] = 0
        clean, audit = clean_transactions(raw)
        self.assertEqual(audit["invalid_rows"], 1)
        self.assertEqual(summary_metrics(clean)["orders"], 2)

    def test_empty_dataset_metrics(self):
        clean, _ = clean_transactions(sample_frame().iloc[:0])
        self.assertEqual(summary_metrics(clean)["sales"], 0)
        self.assertTrue(monthly_sales(clean).empty)

    def test_missing_columns_raise_helpful_error(self):
        with self.assertRaisesRegex(ValueError, "missing required column"):
            validate_columns(pd.DataFrame({"Order ID": ["A-1"]}))


if __name__ == "__main__":
    unittest.main()
