# Retail Sales Analysis and Visualization Using Python

## Title page

**Student name:** [Enter student name]  
**Enrollment number:** [Enter enrollment number]  
**Department:** [Enter department]  
**University:** [Enter university]  
**Academic year:** [Enter academic year]

## Abstract

This project implements an interactive dashboard for the supplied Online Retail transaction workbook. It validates the expected schema, removes exact duplicate rows from the working data, parses dates and numeric measures, classifies eligible positive sales separately from returns, cancellations, and invalid rows, and presents gross sales metrics with filters. The dashboard includes trend, product, country, customer, return, data-quality, and raw-data views. All sales value is computed as quantity multiplied by unit price; it is not profit. Returns and cancellations remain separately visible because the workbook does not provide a universally validated reconciliation to original sale lines.

## 1. Introduction

Retail transaction data can reveal sales patterns by period, product, geography, and identifiable customer. A reusable analysis pipeline and interactive visual interface make these views easier to inspect while documenting the limits of the underlying data.

## 2. Problem statement

The project addresses the difficulty of exploring a large transaction workbook while keeping definitions consistent and making data exclusions and return/cancellation treatment transparent.

## 3. Objectives

- Validate and prepare the provided transaction data without modifying the source workbook.
- Calculate gross positive-sales measures and aggregate trends.
- Compare top products, countries, and identifiable customers.
- Provide combined filters, CSV export, and data-quality details.
- Test core cleaning and aggregation behavior using small synthetic fixtures.

## 4. Dataset description

The workbook is `data/Online Retail.xlsx`. The application checks for `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID`, and `Country` before analysis. Inspection of the supplied workbook found 541,909 data rows, 5,268 exact duplicate rows, 1,454 missing Description values, and 135,080 missing CustomerID values. The date range is 1 December 2010 08:26 through 9 December 2011 12:50. Pandas read InvoiceNo, StockCode, Description, and Country as text/object types; Quantity as int64; InvoiceDate as datetime64; and UnitPrice and CustomerID as float64. The runtime Data Quality section also displays original data types, missing values, and classification counts.

## 5. Methodology

The application loads the first worksheet with OpenPyXL through Pandas, validates the required columns, removes exact duplicate rows, normalizes whitespace in text dimensions, safely parses dates and numeric values, and assigns each remaining row a record type. Vectorized Pandas grouping computes the dashboard metrics. Streamlit applies global filters before downstream KPIs and visualizations are computed.

## 6. Data preprocessing

Rows are classified in order: invoice IDs beginning with `C` are cancellations; valid dated negative-quantity records with positive unit price are returns; valid dated positive-quantity records with positive unit price and a non-cancelled invoice are eligible sales; remaining rows are invalid for those sales metrics. Missing CustomerID is retained in sales totals, but excluded from customer rankings. Exact duplicates retain the first row. The audit records input and post-deduplication counts, classified row counts, invalid price/date counts, original missing values, and date range.

## 7. Exploratory data analysis

The dashboard computes monthly and daily gross sales trends, monthly quantity, top products by quantity and value, country sales and quantity, average sales per invoice, and customer rankings for identifiable customers. The Overview section highlights the highest-sales month and country under current filters. Results update with the global date, country, product, and invoice filters.

## 8. Visualizations and findings

Plotly line charts show monthly and daily trends. Horizontal bars compare products and countries. A donut chart shows the share of gross sales from the leading products. Tooltips expose values and dimensions. Actual workbook analysis under the documented rules found gross positive sales of **£10,642,110.80**, **5,572,420** units, **19,960** distinct sales invoices, **3,922** products, **38** countries, and **4,338** identifiable customers. Average gross sales per eligible invoice were **£533.17**. November 2011 was the strongest month with **£1,503,866.78**. The United Kingdom led country sales with **£9,001,744.09**. There were 9,251 cancellation rows across 3,836 invoice numbers, with £893,979.73 absolute cancellation line value. The separate return count is zero because negative-quantity records in this workbook use cancellation invoice numbers and are classified as cancellations. This cancellation line value is not subtracted from gross sales. These findings are computed from the supplied workbook, not hard-coded in dashboard calculations.

## 9. System design and implementation

- `data_loader.py`: Excel loading and required-column validation.
- `data_cleaning.py`: preparation, record classification, and audit generation.
- `analysis.py`: vectorized metrics and aggregations.
- `app.py`: Streamlit pages, global filters, charts, preview, and CSV export.
- `tests/test_analysis.py`: focused synthetic unit tests.

## 10. Testing

Tests cover gross sales, duplicate removal, date parsing, cancellation identification, missing customer IDs, monthly aggregation, product ranking, empty data, missing columns, and return/sale separation. All eight tests passed with Pytest in the configured 64-bit project environment. Streamlit and Plotly dependencies are also installed. The actual data analysis completed against the supplied workbook using Pandas and OpenPyXL.

## 11. Limitations

No product costs or margin data are available, so profit cannot be inferred. Returns and cancellations are not reconciled into net sales because a validated line-level relationship to original sales is not guaranteed. Invoice counts are not customer counts. Customer analysis necessarily omits rows with missing CustomerID. The analysis is descriptive and cannot establish causal effects or customer satisfaction.

## 12. Conclusion

The application provides a modular and filterable way to inspect the supplied retail transactions while separating eligible gross sales from returns, cancellations, and invalid rows. Its metrics and limitations are documented so the dashboard supports reproducible descriptive analysis.

## 13. References

- Pandas documentation: https://pandas.pydata.org/docs/
- Streamlit documentation: https://docs.streamlit.io/
- Plotly Python documentation: https://plotly.com/python/
- OpenPyXL documentation: https://openpyxl.readthedocs.io/
- Pytest documentation: https://docs.pytest.org/
