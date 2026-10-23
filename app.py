"""Single-page Streamlit dashboard for the supplied India retail orders CSV."""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from analysis import (
    category_sales,
    city_sales,
    monthly_sales,
    region_sales,
    segment_sales,
    ship_mode_sales,
    summary_metrics,
    top_subcategories,
)
from data_cleaning import clean_transactions
from data_loader import load_csv

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "retail_sales_raw.csv"

st.set_page_config(
    page_title="India Retail Sales Analysis",
    page_icon=":material/monitoring:",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data(show_spinner="Reading and preparing the CSV…")
def get_dataset(path: str, modified: float):
    del modified
    return clean_transactions(load_csv(path))


def amount(value):
    return f"{value:,.2f}"


def chart_layout(fig, height=360):
    fig.update_layout(
        height=height,
        margin=dict(l=12, r=12, t=48, b=12),
        font=dict(family="Arial, sans-serif", color="#292524"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend_title_text="",
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="#e7e1d8", zeroline=False)
    return fig


st.title("India Retail Sales Analysis")
st.caption(
    "One view of sales, profit, orders, categories, regions, cities, "
    "customer segments, and data quality. Use the sidebar to filter the dashboard."
)

if not DATA_PATH.exists():
    st.error(f"CSV dataset not found at {DATA_PATH}. Place retail_sales_raw.csv in the project's data folder.")
    st.stop()

try:
    frame, audit = get_dataset(str(DATA_PATH), DATA_PATH.stat().st_mtime)
except Exception as exc:
    st.error(f"The CSV could not be loaded: {exc}")
    st.stop()

with st.sidebar:
    st.header("Dashboard options")
    st.caption("Filters apply to every KPI, chart, table, and export.")

    dates = frame["Order Date"].dropna()
    if dates.empty:
        date_range = None
        st.info("No valid order dates are available.")
    else:
        earliest, latest = dates.min().date(), dates.max().date()
        date_range = st.date_input(
            "Order date range",
            value=(earliest, latest),
            min_value=earliest,
            max_value=latest,
        )

    selected_regions = st.multiselect(
        "Region", sorted(frame["Region"].dropna().unique().tolist()), placeholder="All regions"
    )
    selected_cities = st.multiselect(
        "City", sorted(frame["City"].dropna().unique().tolist()), placeholder="All cities"
    )
    selected_categories = st.multiselect(
        "Category", sorted(frame["Category"].dropna().unique().tolist()), placeholder="All categories"
    )
    selected_segments = st.multiselect(
        "Customer segment",
        sorted(frame["Customer Segment"].dropna().unique().tolist()),
        placeholder="All segments",
    )
    order_query = st.text_input("Search order ID", placeholder="e.g. ORD-10001", icon=":material/search:")
    chart_measure = st.selectbox("Compare charts by", ["Sales", "Profit", "Orders"])

filtered = frame
if date_range and len(date_range) == 2:
    start = pd.Timestamp(date_range[0])
    end = pd.Timestamp(date_range[1]) + pd.Timedelta(days=1) - pd.Timedelta(nanoseconds=1)
    filtered = filtered.loc[filtered["Order Date"].between(start, end)]
if selected_regions:
    filtered = filtered.loc[filtered["Region"].isin(selected_regions)]
if selected_cities:
    filtered = filtered.loc[filtered["City"].isin(selected_cities)]
if selected_categories:
    filtered = filtered.loc[filtered["Category"].isin(selected_categories)]
if selected_segments:
    filtered = filtered.loc[filtered["Customer Segment"].isin(selected_segments)]
if order_query.strip():
    filtered = filtered.loc[filtered["Order ID"].str.contains(order_query.strip(), case=False, na=False)]

if filtered.empty:
    st.warning("No orders match these filters. Adjust the options in the sidebar.")
    st.stop()

metrics = summary_metrics(filtered)
palette = ["#C2410C", "#0F766E", "#2563EB", "#8B5CF6", "#E11D48"]
chart_label = {"Sales": "Sales (source value)", "Profit": "Profit (source value)", "Orders": "Orders"}[chart_measure]

with st.container(horizontal=True):
    st.metric("Sales", amount(metrics["sales"]), border=True)
    st.metric("Profit", amount(metrics["profit"]), border=True)
    st.metric("Orders", f'{metrics["orders"]:,}', border=True)
    st.metric("Units sold", f'{metrics["quantity"]:,}', border=True)

st.caption(
    f"Profit margin: {metrics['profit_margin']:.1%} · "
    f"{metrics['cities']} cities · {metrics['regions']} regions · "
    "values shown as recorded (the CSV does not specify a currency)."
)

monthly = monthly_sales(filtered)
categories = category_sales(filtered)
regions = region_sales(filtered)
cities = city_sales(filtered)
segments = segment_sales(filtered)
ship_modes = ship_mode_sales(filtered)
subcategories = top_subcategories(filtered)

st.subheader("Sales trends")
left, right = st.columns(2)
with left:
    with st.container(border=True):
        fig = px.line(
            monthly,
            x="Month",
            y=chart_measure,
            markers=True,
            title=f"Monthly {chart_measure.lower()}",
            labels={"Month": "Month", chart_measure: chart_label},
        )
        fig.update_traces(line_color=palette[0])
        st.plotly_chart(chart_layout(fig), width="stretch", alt=f"Monthly {chart_measure.lower()} trend")
with right:
    with st.container(border=True):
        fig = px.bar(
            monthly,
            x="Month",
            y=chart_measure,
            title=f"Monthly {chart_measure.lower()} comparison",
            labels={"Month": "Month", chart_measure: chart_label},
            color_discrete_sequence=[palette[1]],
        )
        st.plotly_chart(chart_layout(fig), width="stretch", alt=f"Monthly {chart_measure.lower()} by month")

st.subheader("Category and product performance")
left, right = st.columns(2)
with left:
    with st.container(border=True):
        fig = px.bar(
            categories.sort_values(chart_measure),
            x=chart_measure,
            y="Category",
            orientation="h",
            title=f"{chart_measure} by category",
            labels={chart_measure: chart_label},
            color_discrete_sequence=[palette[0]],
        )
        st.plotly_chart(chart_layout(fig), width="stretch", alt=f"{chart_measure} comparison across categories")
with right:
    with st.container(border=True):
        fig = px.bar(
            subcategories.sort_values(chart_measure),
            x=chart_measure,
            y="Sub-Category",
            orientation="h",
            color="Category",
            title=f"Top sub-categories by {chart_measure.lower()}",
            labels={chart_measure: chart_label},
            color_discrete_sequence=palette,
        )
        st.plotly_chart(chart_layout(fig, 420), width="stretch", alt=f"Top sub-categories by {chart_measure.lower()}")

st.subheader("Region and city performance")
left, right = st.columns(2)
with left:
    with st.container(border=True):
        fig = px.bar(
            regions.sort_values(chart_measure),
            x=chart_measure,
            y="Region",
            orientation="h",
            title=f"{chart_measure} by region",
            labels={chart_measure: chart_label},
            color_discrete_sequence=[palette[1]],
        )
        st.plotly_chart(chart_layout(fig, 400), width="stretch", alt=f"{chart_measure} comparison across regions")
with right:
    with st.container(border=True):
        fig = px.bar(
            cities.head(10).sort_values(chart_measure),
            x=chart_measure,
            y="City",
            orientation="h",
            color="Region",
            title=f"Top 10 cities by {chart_measure.lower()}",
            labels={chart_measure: chart_label},
            color_discrete_sequence=palette,
        )
        st.plotly_chart(chart_layout(fig, 400), width="stretch", alt=f"Top 10 cities by {chart_measure.lower()}")

st.subheader("Customer and shipping options")
left, right = st.columns(2)
with left:
    with st.container(border=True):
        fig = px.bar(
            segments,
            x="Customer Segment",
            y=chart_measure,
            title=f"{chart_measure} by customer segment",
            labels={chart_measure: chart_label},
            color_discrete_sequence=[palette[0]],
        )
        st.plotly_chart(chart_layout(fig), width="stretch", alt=f"{chart_measure} by customer segment")
with right:
    with st.container(border=True):
        fig = px.bar(
            ship_modes,
            x="Ship Mode",
            y=chart_measure,
            title=f"{chart_measure} by ship mode",
            labels={chart_measure: chart_label},
            color_discrete_sequence=[palette[1]],
        )
        st.plotly_chart(chart_layout(fig), width="stretch", alt=f"{chart_measure} by ship mode")

with st.expander("Data quality and cleaning details"):
    quality_cards = st.columns(4)
    for col, label, value in zip(
        quality_cards,
        ["Source rows", "Duplicates removed", "Valid rows", "Invalid rows"],
        [audit["loaded_rows"], audit["duplicate_rows_removed"], audit["valid_rows"], audit["invalid_rows"]],
    ):
        col.metric(label, f"{value:,}")

    st.write(f"**Date range:** {audit['date_min']} to {audit['date_max']}")
    st.write(f"**Rows with negative profit:** {audit['negative_profit_rows']:,}")
    st.write(
        "**Sales differ from quantity × unit price × (1 − discount) by more than 0.02:** "
        f"{audit['sales_calculation_mismatch_rows']:,}"
    )
    st.caption("Sales and Profit are analyzed as supplied; Sales is not overwritten with a recomputed value.")

    left, right = st.columns(2)
    with left:
        st.markdown("**Original CSV column types**")
        types = pd.Series(audit["original_data_types"], name="Type").rename_axis("Column").reset_index()
        st.dataframe(types, width="stretch", hide_index=True, alt="Original CSV column types")
    with right:
        st.markdown("**Missing values in the source CSV**")
        missing = pd.Series(audit["missing_values_by_column"], name="Missing values").rename_axis("Column").reset_index()
        st.dataframe(missing, width="stretch", hide_index=True, alt="Missing values by CSV column")

    st.markdown("**Cleaning rules**")
    st.markdown(
        "- Exact duplicate rows are removed, retaining the first occurrence.\n"
        "- Dates and numeric fields are parsed safely; text dimensions are trimmed.\n"
        "- Valid orders require an order ID, date, region, city, segment, category, sub-category, ship mode, and numeric values.\n"
        "- Quantity must be positive, discount must be between 0 and 1, and source Sales must be nonnegative. Profit may be negative.\n"
        "- The source has no currency column, so values are displayed without a currency conversion or symbol."
    )

with st.expander("Filtered raw data and CSV download"):
    st.caption(f"Showing up to 1,800 of {len(filtered):,} filtered rows. Invalid rows remain available for review.")
    raw_view = filtered.drop(columns=["IsValid"])
    st.dataframe(raw_view, width="stretch", hide_index=True, height=560, alt="Filtered source order rows")
    st.download_button(
        "Download filtered rows as CSV",
        raw_view.to_csv(index=False).encode("utf-8-sig"),
        "retail_sales_filtered.csv",
        "text/csv",
    )
