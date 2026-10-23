# India Retail Sales Analysis and Visualization

## Project details

| Field | Details |
| --- | --- |
| Student | Md Taju |
| Enrollment number | 24TEC2CSML175 |
| Department | Computer Science & Engineering |
| Specialization | Artificial Intelligence & Machine Learning |
| University | Vivekananda Global University (VGU), Jaipur |
| Academic year | 2026–2027 |

## Abstract

This project provides an interactive Streamlit dashboard for the supplied India-focused retail orders CSV. It summarizes sales, profit, orders, units, product categories, customer segments, shipping modes, regions, and cities. The application cleans and validates the provided rows, applies shared dashboard filters, and reports source-data quality without replacing the Sales or Profit fields. The source has no Country or Currency column, so the dashboard uses the supplied Indian region and city labels and displays monetary values without assigning a currency.

## 1. Introduction

Retail transaction data can help describe how orders, product categories, customer segments, and locations contribute to business performance. This project turns the provided order-level CSV into an interactive dashboard where users can filter records and compare summarized measures. It also makes the cleaning rules and important data limitations visible alongside the charts.

## 2. Objectives

- Load and validate the supplied `data/retail_sales_raw.csv` file.
- Summarize source Sales, Profit, order count, and quantity.
- Compare results over time, by category, customer segment, ship mode, region, and city.
- Provide filters that apply consistently across dashboard sections.
- Audit missing values, duplicates, invalid rows, negative profit, and sales formula differences.
- Allow users to inspect and download filtered source rows.

## 3. Dataset description

The application uses only `data/retail_sales_raw.csv`. The CSV contains 1,800 order rows from 1 January 2024 through 30 June 2025. Its 13 columns are:

`Order ID`, `Order Date`, `Region`, `City`, `Customer Segment`, `Category`, `Sub-Category`, `Quantity`, `Unit Price`, `Discount`, `Sales`, `Profit`, and `Ship Mode`.

The file provides four regions and Indian city names. It does not contain a Country or Currency column. Therefore, values are displayed as recorded in the source, without currency symbols or conversions. The analysis does not assume a currency based on the location labels.

## 4. Methodology

The application follows this workflow:

1. Read the CSV as UTF-8 (including an optional byte-order mark) and validate that all expected columns are present.
2. Count source missing values and identify exact duplicate rows.
3. Remove exact duplicates while retaining the first occurrence.
4. Trim text values and parse the date and numeric fields.
5. Mark a row valid when required text and numeric fields exist, the date is valid, quantity is positive, unit price and sales are nonnegative, and discount is in the range 0 to 1.
6. Keep source Sales and Profit values unchanged.
7. Apply date, region, city, category, customer segment, and order-ID filters before producing the dashboard summaries.

The app calculates the sales formula check as `Quantity × Unit Price × (1 − Discount)` and reports rows whose supplied Sales differs from this amount by more than 0.02. This is an audit only; it does not replace Sales.

## 5. Dashboard design

The application presents a single dashboard page rather than switching between separate analysis sections. Four summary cards show Sales, Profit, Orders, and Units Sold. The sidebar keeps the date range, region, city, category, customer segment, and order-ID filters together. A **Compare charts by** selector changes all comparison charts between Sales, Profit, and Orders. The page displays monthly trends, category and sub-category performance, region and city comparisons, customer-segment performance, and ship-mode results together. Data-quality details and filtered raw rows are available in expandable panels below the charts; the raw rows can be downloaded as CSV.

## 6. Results

The figures below are calculated from the supplied CSV with the documented cleaning rules:

| Measure | Result |
| --- | ---: |
| Source rows | 1,800 |
| Exact duplicate rows removed | 0 |
| Valid rows | 1,800 |
| Invalid rows | 0 |
| Date range | 1 Jan 2024 – 30 Jun 2025 |
| Sales, as supplied | 64,511,584.37 |
| Profit, as supplied | 6,285,957.11 |
| Profit margin, Profit ÷ Sales | 9.74% |
| Distinct orders | 1,800 |
| Units | 7,253 |
| Regions / cities | 4 / 16 |
| Categories | 5 |
| Rows with negative profit | 90 |
| Rows with Sales formula difference greater than 0.02 | 220 |

Electronics has the highest total Sales among the categories at 46,326,636.44. East has the highest total Sales among regions at 16,398,072.88. These totals are source values and have no currency assigned by the CSV.

## 7. Data quality and interpretation

The current file has no exact duplicates and all 1,800 rows satisfy the app's validity rules. Ninety rows have negative Profit, which are retained because losses can be valid business outcomes. In 220 rows, the supplied Sales differs from the quantity, unit-price, and discount calculation by more than 0.02. The dashboard preserves those supplied Sales values and exposes the discrepancy in the audit.

Sales and Profit are interpreted as the source's recorded measures. The source file does not specify a currency or calculation policy for its amounts. Profit margin is calculated as the sum of Profit divided by the sum of Sales for the valid, filtered rows.

## 8. Limitations

- No Country or Currency field is present; the app cannot independently validate country assignment or currency.
- The application does not recalculate or normalize Sales and Profit.
- The 220 sales formula differences need source-owner context before their cause can be determined.
- Findings describe only the supplied 2024–2025 CSV and should not be generalized to other periods or businesses.
- The dashboard is descriptive and does not establish causal relationships.

## 9. Implementation and files

- `app.py` — Streamlit interface, filters, charts, data-quality section, and CSV download.
- `data_loader.py` — CSV loading and schema validation.
- `data_cleaning.py` — cleaning rules and data-quality audit.
- `analysis.py` — reusable summary and grouping functions.
- `data/retail_sales_raw.csv` — sole source dataset used by the application.
- `tests/test_analysis.py` — focused tests for the analysis functions.
- `requirements.txt` — Python package requirements.

## 10. Run locally

Use 64-bit Python on Windows, then run these commands from the project folder:

```powershell
py -3.12-64 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Run the analysis tests with `python -m pytest`.

## 11. Render deployment

Deploy the GitHub `main` branch as a Render **Web Service**. Leave Root Directory blank and set:

- Build command: `pip install -r requirements.txt`
- Start command: `streamlit run app.py --server.address 0.0.0.0 --server.port $PORT --server.headless true`
- Environment variables: none required

service URL: [https://dadv-a6-project.mdtaju.tech](https://dadv-a6-project.mdtaju.tech).

The intended custom domain is `dadvproject.mdtaju.tech`. In Render, first add it under **Settings → Custom Domains**. In Cloudflare, create a DNS-only CNAME with Name `dadvproject` and Target `dadv-a6-project.onrender.com` (hostname only; no `https://` or trailing slash). Remove any conflicting AAAA record, then verify the domain in Render. DNS may take a few minutes to propagate. The custom domain should be treated as pending until Render verifies it and issues a valid certificate.

## 12. Conclusion

This project offers a reproducible way to explore the supplied India-focused retail CSV using shared filters and focused summaries. Its data-quality audit preserves the original Sales and Profit fields and makes formula differences visible. The dashboard is designed to communicate what the source supports while clearly documenting missing currency metadata and other limits.

## References

- Pandas documentation: https://pandas.pydata.org/docs/
- Streamlit documentation: https://docs.streamlit.io/
- Plotly Python documentation: https://plotly.com/python/
- Render custom domains: https://render.com/docs/custom-domains
- Render Cloudflare DNS configuration: https://render.com/docs/configure-cloudflare-dns

