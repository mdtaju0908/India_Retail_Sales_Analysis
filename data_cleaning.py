"""Preparation and quality audit for the supplied order-level CSV."""
import pandas as pd

from data_loader import REQUIRED_COLUMNS, validate_columns

TEXT_COLUMNS = [
    "Order ID", "Region", "City", "Customer Segment", "Category",
    "Sub-Category", "Ship Mode",
]
NUMBER_COLUMNS = ["Quantity", "Unit Price", "Discount", "Sales", "Profit"]


def clean_transactions(raw: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Return cleaned orders and an audit without recalculating supplied Sales/Profit."""
    validate_columns(raw)
    original_rows = len(raw)
    missing_values = raw[list(REQUIRED_COLUMNS)].isna().sum().astype(int).to_dict()
    duplicate_mask = raw.duplicated(keep="first")
    frame = raw.loc[~duplicate_mask].copy()

    for column in TEXT_COLUMNS:
        frame[column] = frame[column].astype("string").str.strip()
    frame["Order Date"] = pd.to_datetime(frame["Order Date"], errors="coerce")
    for column in NUMBER_COLUMNS:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")

    text_complete = frame[TEXT_COLUMNS].notna().all(axis=1) & frame[TEXT_COLUMNS].ne("").all(axis=1)
    numeric_complete = frame[NUMBER_COLUMNS].notna().all(axis=1)
    valid = (
        text_complete
        & frame["Order Date"].notna()
        & numeric_complete
        & frame["Quantity"].gt(0)
        & frame["Unit Price"].ge(0)
        & frame["Discount"].between(0, 1)
        & frame["Sales"].ge(0)
    )
    frame["IsValid"] = valid

    calculated = frame["Quantity"] * frame["Unit Price"] * (1 - frame["Discount"])
    sales_mismatch = frame["Sales"].notna() & calculated.notna() & (frame["Sales"] - calculated).abs().gt(0.02)
    audit = {
        "loaded_rows": int(original_rows),
        "original_data_types": {name: str(dtype) for name, dtype in raw.dtypes.items()},
        "duplicate_rows_removed": int(duplicate_mask.sum()),
        "rows_after_deduplication": int(len(frame)),
        "valid_rows": int(valid.sum()),
        "invalid_rows": int((~valid).sum()),
        "negative_profit_rows": int(frame["Profit"].lt(0).sum()),
        "sales_calculation_mismatch_rows": int(sales_mismatch.sum()),
        "missing_values_by_column": missing_values,
        "date_min": frame["Order Date"].min(),
        "date_max": frame["Order Date"].max(),
    }
    return frame, audit
