# Retail Sales Analysis and Visualization Using Python

An interactive data analysis dashboard built with Python, Pandas,
Plotly, and Streamlit to explore historical retail transactions from the
supplied `Online Retail.xlsx` workbook.

## Title Page

  Field                   Details
  ----------------------- ---------------------------------------------
  **Student Name**        Md Taju
  **Enrollment Number**   24TEC2CSML175
  **Department**          Computer Science & Engineering
  **Specialization**      Artificial Intelligence & Machine Learning
  **University**          Vivekananda Global University (VGU), Jaipur
  **Academic Year**       2026--2027

> Update the academic year if your college requires a different session.

## Abstract

This project implements an interactive dashboard for the supplied Online
Retail transaction workbook. It validates the expected schema, removes
exact duplicate rows from the working data, parses dates and numeric
measures, classifies eligible positive sales separately from returns,
cancellations, and invalid rows, and presents gross sales metrics with
filters. The dashboard includes trend, product, country, customer,
return, data-quality, and raw-data views. Sales value is computed as
quantity multiplied by unit price; it is not profit. Returns and
cancellations remain separately visible because the workbook does not
provide a universally validated reconciliation to original sale lines.

## 1. Introduction

Retail transaction data can reveal sales patterns by period, product,
geography, and identifiable customer. A reusable analysis pipeline and
interactive visual interface make these views easier to inspect while
documenting the limits of the underlying data.

This project uses Python-based data analysis and visualization to
transform transaction records into understandable summaries and
interactive charts.

## 2. Problem Statement

Retail businesses generate large volumes of transaction data. Exploring
this data manually can make it difficult to identify sales trends,
high-performing products, country-wise sales, and customer purchasing
patterns. This project addresses that problem by providing a consistent
data-processing workflow and an interactive dashboard, while making data
exclusions and the treatment of returns and cancellations transparent.

## 3. Objectives

-   Validate and prepare the provided transaction data without modifying
    the source workbook.
-   Calculate gross positive-sales measures and aggregate trends.
-   Compare top products, countries, and identifiable customers.
-   Provide combined filters, CSV export, and data-quality details.
-   Test core cleaning and aggregation behavior using small synthetic
    fixtures.
-   Present findings through clear, interactive charts and summary
    metrics.

## 4. Dataset Description

**Dataset file:** `data/Online Retail.xlsx`

The application checks for the following expected columns before
analysis:

-   `InvoiceNo`
-   `StockCode`
-   `Description`
-   `Quantity`
-   `InvoiceDate`
-   `UnitPrice`
-   `CustomerID`
-   `Country`

Inspection of the supplied workbook found:

  Data quality item                        Observed value
  ------------------------------ ------------------------
  Original data rows                              541,909
  Exact duplicate rows                              5,268
  Missing `Description` values                      1,454
  Missing `CustomerID` values                     135,080
  Earliest transaction             1 December 2010, 08:26
  Latest transaction               9 December 2011, 12:50

Pandas read `InvoiceNo`, `StockCode`, `Description`, and `Country` as
text/object types; `Quantity` as `int64`; `InvoiceDate` as `datetime64`;
and `UnitPrice` and `CustomerID` as `float64`. The runtime Data Quality
section displays the actual data types, missing values, and
record-classification counts.

## 5. Methodology

The application follows these main steps:

1.  Load the first worksheet from the Excel workbook using Pandas and
    OpenPyXL.
2.  Validate the required columns.
3.  Remove exact duplicate rows from the working dataset.
4.  Normalize whitespace in relevant text fields.
5.  Parse dates and numeric values safely.
6.  Classify records as sales, returns, cancellations, or invalid
    records.
7.  Calculate metrics and aggregations using vectorized Pandas
    operations.
8.  Apply dashboard filters before updating relevant KPIs, tables, and
    visualizations.
9.  Export selected data where supported.

The original Excel workbook remains unchanged.

## 6. Data Preprocessing

Records are classified in the following order:

-   Invoice IDs beginning with `C` are classified as cancellations.
-   Valid dated negative-quantity records with positive unit price are
    classified as returns, unless already identified as cancellations.
-   Valid dated positive-quantity records with positive unit price and a
    non-cancelled invoice are eligible sales.
-   Remaining records are invalid for the relevant sales metrics.

Missing `CustomerID` values are retained in sales totals but excluded
from customer rankings. Exact duplicates retain the first occurrence.
The data-quality audit reports input and post-deduplication counts,
classified row counts, invalid price/date counts, original missing
values, and the date range.

## 7. Exploratory Data Analysis

The dashboard supports analysis of:

-   Monthly and daily gross sales trends.
-   Monthly quantity sold.
-   Top products by quantity and sales value.
-   Country-wise sales value and quantity.
-   Average gross sales per eligible invoice.
-   Rankings for identifiable customers.
-   Returns and cancellations.
-   Data quality and excluded records.

The overview highlights the highest-sales month and country within the
currently selected filters. Results respond to the global date, country,
product, and invoice filters.

## 8. Visualizations and Findings

The application uses Plotly visualizations, including line charts for
trends, horizontal bar charts for product and country comparisons, and a
donut chart for sales contribution. Tooltips display relevant dimensions
and values.

The analysis of the supplied workbook, using the documented rules,
produced these results:

  Metric                                                    Result
  ----------------------------------------------- ----------------
  Gross positive sales value                        £10,642,110.80
  Units sold                                             5,572,420
  Distinct eligible sales invoices                          19,960
  Products represented in eligible sales                     3,922
  Countries represented in eligible sales                       38
  Identifiable customers                                     4,338
  Average gross sales per eligible invoice                 £533.17
  Strongest month                                    November 2011
  Sales value in strongest month                     £1,503,866.78
  Leading country                                   United Kingdom
  UK sales value                                     £9,001,744.09
  Cancellation rows                                          9,251
  Invoice numbers associated with cancellations              3,836
  Absolute cancellation line value                     £893,979.73

These figures are descriptive results from the supplied workbook under
the stated rules, not hard-coded dashboard calculations. The
cancellation line value is reported separately and is not subtracted
from gross sales. The separate return count is zero under the current
classification because negative-quantity records in this workbook use
cancellation invoice numbers and are classified as cancellations.

**Important interpretation:** Sales value is calculated as
`Quantity × UnitPrice`. It is not profit, because the dataset does not
contain product cost or margin information.

## 9. System Design and Implementation

The application is organized into the following modules:

  -----------------------------------------------------------------------
  File                                Responsibility
  ----------------------------------- -----------------------------------
  `data_loader.py`                    Excel loading and required-column
                                      validation

  `data_cleaning.py`                  Data preparation, record
                                      classification, and audit
                                      generation

  `analysis.py`                       Reusable metrics and aggregations

  `app.py`                            Streamlit dashboard, filters,
                                      charts, preview, and CSV export

  `tests/test_analysis.py`            Focused unit tests using synthetic
                                      test data

  `requirements.txt`                  Python dependencies
  -----------------------------------------------------------------------

## 10. Installation and Execution

### Requirements

-   Python 3.11 or another compatible Python version.
-   The supplied Excel workbook.
-   A terminal or command prompt.

### Setup on Windows PowerShell

Open the project folder in VS Code and run:

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Ensure the workbook is available at:

``` text
data/Online Retail.xlsx
```

Start the dashboard:

``` powershell
streamlit run app.py
```

Streamlit will display a local URL, usually `http://localhost:8501`,
which can be opened in a browser.

Run the tests:

``` powershell
python -m pytest
```

If the project uses Python's built-in `unittest` runner instead, use the
test command documented in the repository.

## 11. Testing

Tests are intended to cover gross sales calculation, duplicate removal,
date parsing, cancellation identification, missing customer IDs, monthly
aggregation, product ranking, empty datasets, missing columns, and the
separation of positive sales and returns.

In the build environment used for the initial implementation, all eight
tests passed with Python's built-in `unittest` runner. Pytest could not
be run because it was not installed, and package installation failed
because the environment could not resolve `pypi.org`. The dashboard
could not be started because Streamlit and Plotly were unavailable for
the same reason. The actual data analysis completed using the available
Pandas and OpenPyXL runtime.

**Re-run the tests and launch the dashboard in your own environment
before submitting the project**, especially if the source code or
dependencies have changed.

## 12. Limitations

-   Product costs and margins are unavailable, so profit cannot be
    calculated.
-   Returns and cancellations are not reconciled into net sales because
    a validated line-level relationship to original sales is not
    guaranteed.
-   Invoice counts are not the same as customer counts.
-   Customer analysis excludes records without `CustomerID`.
-   Results describe the supplied historical dataset and may not
    represent current retail conditions.
-   The analysis is descriptive and does not establish causal
    relationships or customer satisfaction.

## 13. Conclusion

This project provides a modular, filterable way to inspect the supplied
retail transactions while separating eligible gross sales from returns,
cancellations, and invalid records. The dashboard combines summary
metrics, interactive visualizations, product and country comparisons,
customer analysis, and data-quality reporting. Documented metric
definitions and limitations support transparent, reproducible
descriptive analysis.

## 14. Future Enhancements

-   Deploy the dashboard to a suitable hosting platform.
-   Add PDF report generation.
-   Add more advanced customer segmentation if supported by the
    available data.
-   Add sales forecasting only as a separately validated extension.
-   Improve automated data-quality checks and export options.

## 15. References

-   Pandas documentation: https://pandas.pydata.org/docs/
-   Streamlit documentation: https://docs.streamlit.io/
-   Plotly Python documentation: https://plotly.com/python/
-   OpenPyXL documentation: https://openpyxl.readthedocs.io/
-   Pytest documentation: https://docs.pytest.org/
-   UCI Online Retail dataset:
    https://archive.ics.uci.edu/dataset/352/online+retail
