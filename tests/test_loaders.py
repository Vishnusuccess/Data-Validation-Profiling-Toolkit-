import os
import sqlite3
import tempfile

import pandas as pd
import pytest

from datacheckr.loaders import load_from_csv, load_from_parquet, load_from_sql

# Test successful loading of a CSV file
def test_load_csv_success():
    df = pd.DataFrame({"x": [1, 2], "y": ["a", "b"]})
    with tempfile.NamedTemporaryFile(suffix=".csv", mode="w", delete=False) as tmp:
        df.to_csv(tmp.name, index=False)
        loaded = load_from_csv(tmp.name)
    assert df.equals(loaded)
    os.remove(tmp.name)

# Test successful loading of a Parquet file
def test_load_parquet_success():
    df = pd.DataFrame({"a": [1, 2], "b": [True, False]})
    with tempfile.NamedTemporaryFile(suffix=".parquet", delete=False) as tmp:
        df.to_parquet(tmp.name, index=False)
        loaded = load_from_parquet(tmp.name)
    assert df.equals(loaded)
    os.remove(tmp.name)

# Test successful loading of data from an SQL query
def test_load_sql_success():
    conn = sqlite3.connect(":memory:")
    df = pd.DataFrame({"id": [1, 2], "value": ["x", "y"]})
    df.to_sql("test_table", conn, index=False)
    query = "SELECT * FROM test_table"
    loaded = load_from_sql(query, conn)
    assert df.equals(loaded)
    conn.close()

# Test that loading from SQL raises an error for an invalid query
def test_sql_query_failure_raises():
    conn = sqlite3.connect(":memory:")
    with pytest.raises(RuntimeError, match="no such table"):
        load_from_sql("SELECT * FROM nonexistent", conn)
    conn.close()

# Test that loading CSV raises an error when file does not exist
def test_load_csv_file_not_found():
    with pytest.raises(RuntimeError, match="No such file or directory|CSV"):
        load_from_csv("nonexistent.csv")
