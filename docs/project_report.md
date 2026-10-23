# India Retail Sales Analysis

## Abstract

This project uses only the supplied `retail_sales_raw.csv` to provide a filterable Streamlit dashboard and an Excel workbook. It presents sales and profit as recorded in the CSV and compares monthly results, categories, regions, cities, customer segments and shipping modes. A data-quality page documents exclusions and source inconsistencies.

## Dataset

The CSV contains 1,800 order rows and 13 fields: Order ID, Order Date, Region, City, Customer Segment, Category, Sub-Category, Quantity, Unit Price, Discount, Sales, Profit and Ship Mode. Dates run from 1 January 2024 to 30 June 2025. The data contains four regions and 16 cities. It has no Country or Currency column; the India-focused view follows the Indian city names supplied in the file, and numeric values are shown without adding a currency symbol or conversion.

All rows have complete fields and the source contains no exact duplicate rows. All 1,800 rows satisfy the current validation rules. Ninety rows contain negative profit. In 220 rows, the source Sales differs by more than 0.02 from Quantity × Unit Price × (1 − Discount). The dashboard uses the provided Sales and Profit columns without overwriting or reconciling them.

## Method

The CSV loader validates the expected 13 columns. Preparation trims text, parses order dates and numeric measures, removes exact duplicate rows from the working frame and flags valid orders. An order is valid when required dimensions are present, numeric measures and date parse successfully, quantity is positive, unit price is nonnegative, discount is between 0 and 1, and source sales are nonnegative. Negative profit is retained.

Pandas aggregations calculate totals and group results by month, region, city, category, sub-category, customer segment and shipping mode. Streamlit filters all views by date, region, city, category, segment and order ID. Plotly displays monthly trends, category mix, and regional, city, segment and shipping comparisons.

## Metrics

For the supplied data, total Sales is 64,511,584.37, total Profit is 6,285,957.11, profit margin is 9.74%, order count is 1,800, and units sum to 7,253. These totals are generated from the source Sales and Profit fields; currency is unspecified.

## Workbook

The output workbook contains Overview, Region Summary, City Summary, Category Summary, Monthly Summary and Raw Data. The Raw Data sheet includes all 1,800 supplied rows and 13 original columns. Summary sheets aggregate valid rows.

## Limitations

The source does not identify currency or include an explicit Country field. The region and city labels are used for the India-focused analysis. Sales differs from the simple quantity-price-discount calculation for some rows; the provided Sales value remains authoritative for dashboard totals, and the mismatch count is disclosed. The analysis is descriptive and does not establish cause and effect.

## Verification

Automated tests cover source-column validation, duplicate removal, date and monthly aggregation, category totals, negative-profit retention, invalid quantity exclusion and empty data. Run them with `\.venv\Scripts\python.exe -m pytest` from the project directory.
