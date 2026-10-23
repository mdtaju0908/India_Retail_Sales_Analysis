"""Aggregations for order, profit, category, region and city analysis."""
import pandas as pd


def sales_rows(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.loc[frame["IsValid"]]


def summary_metrics(frame: pd.DataFrame) -> dict:
    valid = sales_rows(frame)
    total_sales = float(valid["Sales"].sum())
    total_profit = float(valid["Profit"].sum())
    return {
        "sales": total_sales,
        "profit": total_profit,
        "profit_margin": total_profit / total_sales if total_sales else 0.0,
        "orders": int(valid["Order ID"].nunique()),
        "quantity": int(valid["Quantity"].sum()),
        "regions": int(valid["Region"].nunique()),
        "cities": int(valid["City"].nunique()),
        "categories": int(valid["Category"].nunique()),
        "average_discount": float(valid["Discount"].mean()) if not valid.empty else 0.0,
    }


def monthly_sales(frame: pd.DataFrame) -> pd.DataFrame:
    valid = sales_rows(frame)
    if valid.empty:
        return pd.DataFrame(columns=["Month", "Sales", "Profit", "Orders", "Quantity"])
    grouped = valid.assign(Month=valid["Order Date"].dt.to_period("M").dt.to_timestamp())
    return grouped.groupby("Month", as_index=False).agg(
        Sales=("Sales", "sum"), Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique"), Quantity=("Quantity", "sum"),
    )


def category_sales(frame: pd.DataFrame) -> pd.DataFrame:
    valid = sales_rows(frame)
    return valid.groupby("Category", as_index=False).agg(
        Sales=("Sales", "sum"), Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique"), Quantity=("Quantity", "sum"),
    ).sort_values("Sales", ascending=False)


def region_sales(frame: pd.DataFrame) -> pd.DataFrame:
    valid = sales_rows(frame)
    return valid.groupby("Region", as_index=False).agg(
        Sales=("Sales", "sum"), Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique"), Cities=("City", "nunique"),
    ).sort_values("Sales", ascending=False)


def city_sales(frame: pd.DataFrame) -> pd.DataFrame:
    valid = sales_rows(frame)
    return valid.groupby(["Region", "City"], as_index=False).agg(
        Sales=("Sales", "sum"), Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique"), Quantity=("Quantity", "sum"),
    ).sort_values("Sales", ascending=False)


def segment_sales(frame: pd.DataFrame) -> pd.DataFrame:
    valid = sales_rows(frame)
    return valid.groupby("Customer Segment", as_index=False).agg(
        Sales=("Sales", "sum"), Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique"),
    ).sort_values("Sales", ascending=False)


def top_subcategories(frame: pd.DataFrame, limit: int = 10) -> pd.DataFrame:
    valid = sales_rows(frame)
    result = valid.groupby(["Category", "Sub-Category"], as_index=False).agg(
        Sales=("Sales", "sum"), Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum"), Orders=("Order ID", "nunique"),
    )
    return result.sort_values("Sales", ascending=False).head(limit)


def ship_mode_sales(frame: pd.DataFrame) -> pd.DataFrame:
    valid = sales_rows(frame)
    return valid.groupby("Ship Mode", as_index=False).agg(
        Sales=("Sales", "sum"), Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique"),
    ).sort_values("Sales", ascending=False)
