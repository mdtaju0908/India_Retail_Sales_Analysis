"""CSV loading and schema validation for the India retail orders dataset."""
from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = (
    "Order ID", "Order Date", "Region", "City", "Customer Segment",
    "Category", "Sub-Category", "Quantity", "Unit Price", "Discount",
    "Sales", "Profit", "Ship Mode",
)


def validate_columns(frame: pd.DataFrame) -> None:
    missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(
            "Dataset is missing required column(s): " + ", ".join(missing)
            + ". Expected: " + ", ".join(REQUIRED_COLUMNS)
        )


def load_csv(path: str | Path) -> pd.DataFrame:
    """Read the supplied CSV and verify its transaction schema."""
    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(f"CSV dataset not found: {source}")
    try:
        frame = pd.read_csv(source, encoding="utf-8-sig", low_memory=False)
    except Exception as exc:
        raise ValueError(f"Could not read CSV dataset '{source}': {exc}") from exc
    validate_columns(frame)
    return frame
