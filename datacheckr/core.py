import argparse
import sqlite3
import sys

import pandas as pd

from datacheckr.loaders import load_from_csv, load_from_parquet, load_from_sql
from datacheckr.reporters import generate_markdown_report


def validate_dataframe(df: pd.DataFrame) -> dict:
    """
    Perform basic data validation and profiling on a DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame to validate.

    Returns:
        dict: A dictionary containing various statistics and checks.

    Raises:
        ValueError: If the input is not a pandas DataFrame.
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame.")

    if df.empty:
        return {
            "shape": (0, 0),
            "message": "Empty DataFrame provided. No profiling applied.",
            "validations": []
        }

    result = {
        "shape": df.shape,
        "nulls": df.isnull().sum().to_dict(),
        "dtypes": df.dtypes.apply(str).to_dict(),
        "unique_values": df.nunique().to_dict(),
        "missing_pct": (df.isnull().mean() * 100).round(2).to_dict(),
        "validations": []
    }

    # Correct structure for tests: describe().transpose()
    numeric_cols = df.select_dtypes(include="number")
    result["descriptive_stats"] = numeric_cols.describe().transpose().to_dict()

    # Validation rules
    required_columns = ["id", "name", "score"]
    for col in required_columns:
        if col not in df.columns:
            result["validations"].append(f"Missing required column: '{col}'")

    for col in ["id", "name"]:
        if col in df.columns and df[col].isnull().any():
            result["validations"].append(f"Column '{col}' should not have nulls.")

    if "id" in df.columns and not df["id"].is_unique:
        result["validations"].append("Column 'id' must contain unique values.")

    if "score" in df.columns:
        invalid_scores = df["score"].dropna().apply(lambda x: not (0 <= x <= 100))
        if invalid_scores.any():
            result["validations"].append("Some scores are outside the range 0–100.")

    return result


def main(args=None):
    parser = argparse.ArgumentParser(description="Data validation and profiling tool.")
    parser.add_argument("type", choices=["csv", "parquet", "sql"], help="Type of input data.")
    parser.add_argument("path", help="Path to the data file or SQL database.")
    parser.add_argument("--query", help="SQL SELECT query to run (required if type is 'sql').")

    args = parser.parse_args(args)

    try:
        if args.type == "csv":
            df = load_from_csv(args.path)
        elif args.type == "parquet":
            df = load_from_parquet(args.path)
        elif args.type == "sql":
            if not args.query:
                print("Error: --query is required when using 'sql' as type.")
                sys.exit(1)
            with sqlite3.connect(args.path) as conn:
                df = load_from_sql(args.query, conn)
        else:
            print("Unsupported file type.", file=sys.stderr)
            sys.exit(1)


        result = validate_dataframe(df)
        print(result)
        generate_markdown_report(result)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
