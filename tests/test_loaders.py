import os
import sqlite3
import tempfile

import pandas as pd
import pytest

from datacheckr.loaders import load_from_csv, load_from_parquet, load_from_sql


def test_load_csv_success():
    df = pd.DataFrame({"x": [1, 2], "y": ["a", "b"]})
    with tempfile.NamedTemporaryFile(suffix=".csv", mode="w", delete=False) as tmp:
        df.to_csv(tmp.name, index=False)
        loaded = load_from_csv(tmp.name)
    assert df.equals(loaded)
    os.remove(tmp.name)


def test_load_parquet_success():
    df = pd.DataFrame({"a": [1, 2], "b": [True, False]})
    with tempfile.NamedTemporaryFile(suffix=".parquet", delete=False) as tmp:
        df.to_parquet(tmp.name, index=False)
        loaded = load_from_parquet(tmp.name)
    assert df.equals(loaded)
    os.remove(tmp.name)


def test_load_sql_success():
    conn = sqlite3.connect(":memory:")
    df = pd.DataFrame({"id": [1, 2], "value": ["x", "y"]})
    df.to_sql("test_table", conn, index=False)
    query = "SELECT * FROM test_table"
    loaded = load_from_sql(query, conn)
    assert df.equals(loaded)
    conn.close()


def test_sql_query_failure_raises():
    conn = sqlite3.connect(":memory:")
    with pytest.raises(RuntimeError, match="no such table"):
        load_from_sql("SELECT * FROM nonexistent", conn)
    conn.close()


def test_load_csv_file_not_found():
    with pytest.raises(RuntimeError, match="No such file or directory|CSV"):
        load_from_csv("nonexistent.csv")
