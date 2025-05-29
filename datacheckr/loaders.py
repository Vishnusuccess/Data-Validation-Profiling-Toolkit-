import sqlite3

import pandas as pd


def load_from_csv(path: str) -> pd.DataFrame:
    """
    Load a CSV file into a DataFrame.

    Args:
        path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: The loaded DataFrame.

    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.ParserError: If the file cannot be parsed.
    """
    try:
        return pd.read_csv(path)
    except Exception as e:
        raise RuntimeError(f"Failed to load CSV: {e}")


def load_from_parquet(path: str) -> pd.DataFrame:
    """
    Load a Parquet file into a DataFrame.

    Args:
        path (str): Path to the Parquet file.

    Returns:
        pd.DataFrame: The loaded DataFrame.

    Raises:
        ImportError: If required parquet engine is missing.
        FileNotFoundError: If the file does not exist.
    """
    try:
        return pd.read_parquet(path)
    except Exception as e:
        raise RuntimeError(f"Failed to load Parquet: {e}")


def load_from_sql(query: str, connection: sqlite3.Connection) -> pd.DataFrame:
    """
    Load a DataFrame from an SQL query using a given connection.

    Args:
        query (str): SQL SELECT query string.
        connection (sqlite3.Connection): Open database connection.

    Returns:
        pd.DataFrame: Result of the query as a DataFrame.

    Raises:
        ValueError: If the query returns no rows.
        Exception: For SQL errors or connection issues.
    """
    try:
        df = pd.read_sql_query(query, connection)
        if df.empty:
            raise ValueError("Query executed but returned no data.")
        return df
    except Exception as e:
        raise RuntimeError(f"Failed to execute SQL query: {e}")
