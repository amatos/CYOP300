import pandas as pd
import pytest

import load_data


def test_load_csv_returns_dataframe_when_file_exists(tmp_path):
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text("a,b\n1,2\n3,4\n")

    df = load_data.load_csv(str(csv_file))

    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["a", "b"]
    assert df.shape == (2, 2)


def test_load_csv_reads_expected_values(tmp_path):
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text("x,y\n10,20\n30,40\n")

    df = load_data.load_csv(str(csv_file))

    assert df["x"].tolist() == [10, 30]
    assert df["y"].tolist() == [20, 40]


def test_load_csv_raises_file_not_found_for_missing_file(tmp_path):
    missing_file = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_data.load_csv(str(missing_file))


def test_load_csv_raises_file_not_found_for_empty_path():
    with pytest.raises(FileNotFoundError):
        load_data.load_csv("")
