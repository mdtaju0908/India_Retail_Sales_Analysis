# India Retail Sales Analysis

An interactive Streamlit dashboard for exploring the supplied India-focused retail orders CSV. The app shows sales, profit, orders, quantities, product categories, customer segments, Indian regions and cities, and data quality. It reads only `data/retail_sales_raw.csv`.

## Dashboard

- Custom domain being configured: `https://dad-a6-project.mdtaju.tech`

The custom domain works after its Cloudflare DNS record is valid and the hostname is added and verified in Render. See [Deployment](#deployment).

## Dataset

**File:** `data/retail_sales_raw.csv`

The source contains these columns: Order ID, Order Date, Region, City, Customer Segment, Category, Sub-Category, Quantity, Unit Price, Discount, Sales, Profit, and Ship Mode. The dashboard does not load the previous workbook or any other dataset.

The file contains 1,800 order rows dated 1 January 2024 through 30 June 2025. It contains Indian regions and cities, but no Country or Currency column. Accordingly, the dashboard labels monetary figures as source values and does not add a currency symbol or convert values.

## Features

- Summary metrics for sales, profit, orders, units, and profit margin.
- Monthly sales and profit trends.
- Category and sub-category comparisons.
- Region and city analysis.
- Customer segment and ship-mode summaries.
- Filters for date, region, city, category, customer segment, and order ID.
- A data-quality audit and downloadable filtered CSV.

## Data handling

The app removes exact duplicate rows while retaining the first occurrence, trims text fields, and parses dates and numeric columns. It marks a row valid when its required text and numeric fields are present, the date parses, quantity is positive, unit price and sales are nonnegative, and discount is between 0 and 1. Invalid source rows remain available in the Raw data view.

Sales and Profit are analyzed as provided in the CSV. Sales is not replaced with a recomputed amount. The audit reports rows where Sales differs by more than 0.02 from Quantity × Unit Price × (1 − Discount), as well as rows with negative profit.

## Project snapshot

Figures below are calculated from the supplied CSV using the app's cleaning rules:

| Measure | Value |
| --- | ---: |
| Source rows | 1,800 |
| Valid rows | 1,800 |
| Exact duplicates removed | 0 |
| Date range | 1 Jan 2024 – 30 Jun 2025 |
| Sales (source values) | 64,511,584.37 |
| Profit (source values) | 6,285,957.11 |
| Orders | 1,800 |
| Units sold | 7,253 |
| Regions / cities | 4 / 16 |
| Rows with negative profit | 90 |
| Sales formula mismatch rows | 220 |

The source file does not specify a currency, so these totals intentionally have no currency symbol. The formula mismatch count is an audit finding; it does not cause the app to overwrite source Sales values.

## Run locally on Windows

Use a 64-bit Python installation. The earlier 32-bit Python environment could not install compatible Pandas wheels. Check installed Python runtimes with `py -0p`, then create the environment with an available 64-bit version (for example, Python 3.12 64-bit):

```powershell
cd "C:\path\to\retail-sales-analysis"
py -3.12-64 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Keep the CSV at `data/retail_sales_raw.csv`. Streamlit prints a local address, usually `http://localhost:8501`.

Run the analysis tests with:

```powershell
python -m pytest
```

## Deployment on Render

Create a **Web Service** connected to this GitHub repository and use:

| Setting | Value |
| --- | --- |
| Branch | `main` |
| Root Directory | Leave blank |
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `streamlit run app.py --server.address 0.0.0.0 --server.port $PORT --server.headless true` |
| Environment Variables | None required |

Render provides the `PORT` value. The app must listen on `0.0.0.0` and that port for Render to route web traffic correctly. The free instance can spin down after inactivity.

### Connect `dadvproject.mdtaju.tech`

1. In the Render service, open **Settings → Custom Domains** and add `dadvproject.mdtaju.tech`.
2. In Cloudflare DNS, add a **CNAME** record:
   - **Name:** `dadvproject`
   - **Target:** `dadv-a6-project.onrender.com`
   - **Proxy status:** DNS only while Render verifies the domain and issues its certificate.
3. Enter only the hostname as the target. Do not include `https://` or a trailing slash.
4. Remove any conflicting `AAAA` record for this hostname, then use **Verify** in Render. DNS propagation may take a few minutes.
5. After Render reports the domain and certificate as valid, Cloudflare proxying can optionally be enabled.

## Project files

```text
app.py                 Streamlit dashboard
analysis.py            Aggregations and summary metrics
data_cleaning.py       Cleaning rules and quality audit
data_loader.py         CSV loading and schema validation
data/retail_sales_raw.csv  Supplied source dataset
docs/project_report.md Academic project report
tests/test_analysis.py Analysis tests
requirements.txt       Python dependencies
```

Generated workbooks and other files in `outputs/` are local artifacts and are not included in the Git repository.
