import pandas as pd
import pytest
from unittest import mock
from datacheckr.core import validate_dataframe, main


def test_validate_normal_dataframe():
    df = pd.DataFrame({
        "id": [1, 2, 3, 4],
        "name": ["Alice", "Bob", "Charlie", "Dana"],
        "score": [85.5, 90.0, 92.0, 88.0]
    })

    result = validate_dataframe(df)

    assert result["shape"] == (4, 3)
    assert result["nulls"]["score"] == 0
    assert result["missing_pct"]["score"] == 0.0

    stats = result["descriptive_stats"]
    assert "mean" in stats
    assert "score" in stats["mean"]
    expected_mean = sum([85.5, 90.0, 92.0, 88.0]) / 4
    assert stats["mean"]["score"] == pytest.approx(expected_mean)

    assert isinstance(result["validations"], list)
    assert len(result["validations"]) == 0



def test_validate_empty_dataframe():
    df = pd.DataFrame()
    result = validate_dataframe(df)
    assert result["shape"] == (0, 0)
    assert "message" in result
    assert "Empty DataFrame" in result["message"]
    assert "validations" in result


def test_invalid_input_raises_error():
    with pytest.raises(ValueError):
        validate_dataframe("not a dataframe")


def test_missing_required_column():
    df = pd.DataFrame({
        "id": [1, 2, 3, 4],
        "score": [90, 85, 88, 95]  # 'name' column missing
    })
    result = validate_dataframe(df)
    assert any("Missing required column: 'name'" in v for v in result["validations"])


@mock.patch("sys.argv", ["core.py", "csv", "tests/sample.csv"])
@mock.patch("datacheckr.core.load_from_csv")
@mock.patch("datacheckr.core.generate_markdown_report")
def test_main_csv(mock_report, mock_loader):
    df = pd.DataFrame({
        "id": [1, 2],
        "name": ["A", "B"],
        "score": [90, 95]
    })
    mock_loader.return_value = df
    main()
    mock_report.assert_called_once()


@mock.patch("sys.argv", ["core.py", "parquet", "tests/sample.parquet"])
@mock.patch("datacheckr.core.load_from_parquet")
@mock.patch("datacheckr.core.generate_markdown_report")
def test_main_parquet(mock_report, mock_loader):
    df = pd.DataFrame({"id": [1], "name": ["X"], "score": [100]})
    mock_loader.return_value = df
    main()
    mock_report.assert_called_once()


@mock.patch("sys.argv", ["core.py", "sql", "fake.db", "--query", "SELECT * FROM table"])
@mock.patch("sqlite3.connect")
@mock.patch("datacheckr.core.load_from_sql")
@mock.patch("datacheckr.core.generate_markdown_report")
def test_main_sql(mock_report, mock_sql_loader, mock_connect):
    df = pd.DataFrame({"id": [1], "name": ["Y"], "score": [85]})
    mock_sql_loader.return_value = df
    mock_connect.return_value.__enter__.return_value = mock.Mock()
    main()
    mock_report.assert_called_once()


@mock.patch("sys.argv", ["core.py", "sql", "fake.db"])
def test_main_sql_missing_query(monkeypatch, capsys):
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "Error: --query is required" in captured.out


@mock.patch("sys.argv", ["core.py", "unsupported", "path"])
def test_main_unsupported_filetype(capsys):
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "invalid choice" in captured.err
    assert "'unsupported'" in captured.err




@mock.patch("sys.argv", ["core.py", "csv", "missing.csv"])
@mock.patch("datacheckr.core.load_from_csv", side_effect=RuntimeError("File not found"))
def test_main_loader_exception(mock_loader, capsys):
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "Error: File not found" in captured.out
