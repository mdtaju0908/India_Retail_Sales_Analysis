"""Streamlit dashboard for the supplied India retail orders CSV."""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from analysis import category_sales, city_sales, monthly_sales, region_sales, segment_sales, ship_mode_sales, summary_metrics, top_subcategories
from data_cleaning import clean_transactions
from data_loader import load_csv

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "retail_sales_raw.csv"

st.set_page_config(page_title="India Retail Sales Analysis", page_icon=":material/monitoring:", layout="wide", initial_sidebar_state="expanded")


@st.cache_data(show_spinner="Reading and preparing the CSV…")
def get_dataset(path: str, modified: float):
    del modified
    return clean_transactions(load_csv(path))


def amount(value):
    return f"{value:,.2f}"


def chart_layout(fig, height=380):
    fig.update_layout(height=height, margin=dict(l=12, r=12, t=48, b=12), font=dict(family="Arial, sans-serif", color="#292524"), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="#e7e1d8", zeroline=False)
    return fig


st.title("India Retail Sales Analysis")
st.caption("Explore orders, sales, profit, categories and Indian regions from the supplied CSV.")
if not DATA_PATH.exists():
    st.error(f"CSV dataset not found at {DATA_PATH}. Place retail_sales_raw.csv in the project's data folder.")
    st.stop()

try:
    frame, audit = get_dataset(str(DATA_PATH), DATA_PATH.stat().st_mtime)
except Exception as exc:
    st.error(f"The CSV could not be loaded: {exc}")
    st.stop()

with st.sidebar:
    st.header("Explore")
    section = st.radio("Dashboard", ["Overview", "Sales trends", "Category analysis", "Region & city", "Customer segments", "Data quality", "Raw data"])
    st.divider()
    st.subheader("Filters")
    dates = frame["Order Date"].dropna()
    if dates.empty:
        date_range = None
        st.info("No valid order dates are available.")
    else:
        earliest, latest = dates.min().date(), dates.max().date()
        date_range = st.date_input("Order date range", value=(earliest, latest), min_value=earliest, max_value=latest)
    selected_regions = st.multiselect("Region", sorted(frame["Region"].dropna().unique().tolist()), placeholder="All regions")
    selected_cities = st.multiselect("City", sorted(frame["City"].dropna().unique().tolist()), placeholder="All cities")
    selected_categories = st.multiselect("Category", sorted(frame["Category"].dropna().unique().tolist()), placeholder="All categories")
    selected_segments = st.multiselect("Customer segment", sorted(frame["Customer Segment"].dropna().unique().tolist()), placeholder="All segments")
    order_query = st.text_input("Search order ID", placeholder="e.g. ORD-10001", icon=":material/search:")

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
    st.warning("No orders match these filters. Adjust the filters in the sidebar.")
    st.stop()

metrics = summary_metrics(filtered)
palette = ["#C2410C", "#0F766E", "#2563EB", "#8B5CF6", "#E11D48"]

if section == "Overview":
    st.subheader("Performance at a glance")
    cols = st.columns(4)
    for col, label, value in zip(cols, ["Sales", "Profit", "Orders", "Units sold"], [amount(metrics["sales"]), amount(metrics["profit"]), f'{metrics["orders"]:,}', f'{metrics["quantity"]:,}']):
        col.metric(label, value)
    st.caption(f"Profit margin: {metrics['profit_margin']:.1%} · {metrics['cities']} cities · {metrics['regions']} regions · values shown as recorded (CSV does not specify a currency).")
    monthly, categories_df = monthly_sales(filtered), category_sales(filtered)
    left, right = st.columns([1.4, 1])
    with left:
        fig = px.line(monthly, x="Month", y="Sales", markers=True, title="Monthly sales", labels={"Month":"Month", "Sales":"Sales (source value)"})
        fig.update_traces(line_color=palette[0], hovertemplate="%{x|%b %Y}<br>%{y:,.2f}<extra></extra>")
        st.plotly_chart(chart_layout(fig), width="stretch")
    with right:
        fig = px.pie(categories_df, values="Sales", names="Category", hole=.58, title="Sales mix by category")
        fig.update_traces(textposition="inside", textinfo="percent", hovertemplate="%{label}<br>%{value:,.2f}<extra></extra>")
        st.plotly_chart(chart_layout(fig), width="stretch")
    st.info("This file lists Indian cities and regions but has no Country or Currency column. Sales and profit use the source values; they are not recalculated or converted.")

elif section == "Sales trends":
    st.subheader("Sales and profit over time")
    monthly = monthly_sales(filtered)
    if monthly.empty:
        st.info("No valid orders in this date range.")
    else:
        best = monthly.loc[monthly["Sales"].idxmax()]
        a, b = st.columns(2)
        a.metric("Highest sales month", f"{best['Month']:%B %Y}", amount(best["Sales"]))
        b.metric("Average discount", f"{metrics['average_discount']:.1%}")
        left, right = st.columns(2)
        with left:
            fig = px.line(monthly, x="Month", y="Sales", markers=True, title="Monthly sales", labels={"Sales":"Sales (source value)"})
            st.plotly_chart(chart_layout(fig), width="stretch")
        with right:
            fig = px.bar(monthly, x="Month", y="Profit", title="Monthly profit", labels={"Profit":"Profit (source value)"}, color_discrete_sequence=[palette[1]])
            st.plotly_chart(chart_layout(fig), width="stretch")
        st.dataframe(monthly.assign(Month=monthly["Month"].dt.strftime("%b %Y"), Sales=monthly["Sales"].map(amount), Profit=monthly["Profit"].map(amount)), width="stretch", hide_index=True)

elif section == "Category analysis":
    st.subheader("Category and sub-category performance")
    category = category_sales(filtered)
    left, right = st.columns(2)
    with left:
        fig = px.bar(category.sort_values("Sales"), x="Sales", y="Category", orientation="h", title="Sales by category", color_discrete_sequence=[palette[0]])
        st.plotly_chart(chart_layout(fig, 420), width="stretch")
    with right:
        fig = px.bar(top_subcategories(filtered).sort_values("Sales"), x="Sales", y="Sub-Category", orientation="h", title="Top sub-categories by sales", color="Category", color_discrete_sequence=palette)
        st.plotly_chart(chart_layout(fig, 420), width="stretch")
    st.dataframe(category.assign(Sales=category["Sales"].map(amount), Profit=category["Profit"].map(amount)), width="stretch", hide_index=True)

elif section == "Region & city":
    st.subheader("Regional and city performance")
    regional, cities_df = region_sales(filtered), city_sales(filtered)
    left, right = st.columns(2)
    with left:
        fig = px.bar(regional.sort_values("Sales"), x="Sales", y="Region", orientation="h", title="Sales by region", color_discrete_sequence=[palette[0]])
        st.plotly_chart(chart_layout(fig, 420), width="stretch")
    with right:
        fig = px.bar(cities_df.head(10).sort_values("Sales"), x="Sales", y="City", orientation="h", title="Top cities by sales", color="Region", color_discrete_sequence=palette)
        st.plotly_chart(chart_layout(fig, 420), width="stretch")
    st.dataframe(cities_df.assign(Sales=cities_df["Sales"].map(amount), Profit=cities_df["Profit"].map(amount)), width="stretch", hide_index=True)

elif section == "Customer segments":
    st.subheader("Customer segments and shipping")
    left, right = st.columns(2)
    seg, ship = segment_sales(filtered), ship_mode_sales(filtered)
    with left:
        fig = px.bar(seg, x="Customer Segment", y="Sales", title="Sales by customer segment", color_discrete_sequence=[palette[0]])
        st.plotly_chart(chart_layout(fig), width="stretch")
    with right:
        fig = px.bar(ship, x="Ship Mode", y="Orders", title="Orders by ship mode", color_discrete_sequence=[palette[1]])
        st.plotly_chart(chart_layout(fig), width="stretch")
    st.dataframe(seg.assign(Sales=seg["Sales"].map(amount), Profit=seg["Profit"].map(amount)), width="stretch", hide_index=True)

elif section == "Data quality":
    st.subheader("Data quality and preparation")
    cols = st.columns(4)
    for col, label, value in zip(cols, ["Source rows", "Duplicates removed", "Valid rows", "Invalid rows"], [audit["loaded_rows"], audit["duplicate_rows_removed"], audit["valid_rows"], audit["invalid_rows"]]):
        col.metric(label, f"{value:,}")
    st.write(f"**Date range:** {audit['date_min']} to {audit['date_max']}")
    st.write(f"**Rows with negative profit:** {audit['negative_profit_rows']:,}")
    st.write(f"**Sales differ from quantity × unit price × (1 − discount) by more than 0.02:** {audit['sales_calculation_mismatch_rows']:,}")
    st.caption("The supplied Sales and Profit columns are analyzed as provided. Sales is not overwritten with a recomputed value.")
    st.markdown("**Original CSV column types**")
    st.dataframe(pd.Series(audit["original_data_types"], name="Type").rename_axis("Column").reset_index(), width="stretch", hide_index=True)
    st.markdown("**Missing values in the source CSV**")
    missing = pd.Series(audit["missing_values_by_column"], name="Missing values").rename_axis("Column").reset_index()
    st.dataframe(missing, width="stretch", hide_index=True)
    st.markdown("**Cleaning rules**")
    st.markdown("- Exact duplicate rows are removed, retaining the first occurrence.\n- Dates and numeric fields are parsed safely; text dimensions are trimmed.\n- Valid orders require an order ID, date, region, city, segment, category, sub-category, ship mode and numeric values.\n- Quantity must be positive, discount must be between 0 and 1, and source sales must be nonnegative. Profit may be negative.\n- Currency is not specified in the source file, so values are displayed without a currency conversion or symbol.")

elif section == "Raw data":
    st.subheader("Filtered source rows")
    st.caption(f"Showing up to 1,800 of {len(filtered):,} filtered rows. Values come from the supplied CSV; invalid rows remain visible for review.")
    raw_view = filtered.drop(columns=["IsValid"])
    st.dataframe(raw_view, width="stretch", hide_index=True, height=560)
    st.download_button("Download filtered rows as CSV", raw_view.to_csv(index=False).encode("utf-8-sig"), "retail_sales_filtered.csv", "text/csv")
