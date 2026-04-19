import pandas as pd
import pytest
from unittest.mock import patch

import lab5ui


@pytest.fixture
def pop_df():
    return pd.DataFrame(
        {
            "Pop Apr 1": [100.0, 200.0, 300.0],
            "Pop Jul 1": [110.0, 210.0, 310.0],
            "Change Pop": [10.0, 10.0, 10.0],
        }
    )


@pytest.fixture
def housing_df():
    return pd.DataFrame(
        {
            "AGE": [10.0, 20.0, 30.0],
            "BEDRMS": [2.0, 3.0, 4.0],
            "BUILT": [1990.0, 2000.0, 2010.0],
            "ROOMS": [5.0, 6.0, 7.0],
            "UTILITY": [100.0, 200.0, 300.0],
        }
    )


def test_compute_statistics_prints_expected_values(capsys):
    series = pd.Series([1.0, 2.0, 3.0, 4.0])

    lab5ui.compute_statistics(series)

    output = capsys.readouterr().out
    assert "Count" in output
    assert "Mean" in output
    assert "Standard Deviation" in output
    assert "Min" in output
    assert "Max" in output


def test_compute_statistics_handles_nan(capsys):
    series = pd.Series([1.0, float("nan"), 3.0])

    lab5ui.compute_statistics(series)

    output = capsys.readouterr().out
    assert "Count" in output
    assert "2" in output


@patch("lab5ui.pyplot.show")
@patch("lab5ui.pyplot.tight_layout")
@patch("lab5ui.pyplot.ylabel")
@patch("lab5ui.pyplot.xlabel")
@patch("lab5ui.pyplot.title")
@patch("lab5ui.pyplot.hist")
@patch("lab5ui.pyplot.figure")
def test_display_histogram_calls_matplotlib(
    mock_figure,
    mock_hist,
    mock_title,
    mock_xlabel,
    mock_ylabel,
    mock_tight_layout,
    mock_show,
):
    series = pd.Series([1.0, 2.0, 3.0])

    lab5ui.display_histogram(series, "AGE", "Housing Data")

    mock_figure.assert_called_once()
    mock_hist.assert_called_once()
    mock_title.assert_called_once()
    mock_xlabel.assert_called_once_with("AGE", fontsize=12)
    mock_ylabel.assert_called_once_with("Frequency", fontsize=12)
    mock_tight_layout.assert_called_once()
    mock_show.assert_called_once()


@patch("lab5ui.display_histogram")
@patch("lab5ui.compute_statistics")
def test_select_dataset_column_exits_immediately(mock_stats, mock_hist, pop_df, capsys):
    with patch("lab5ui.inquirer.select") as mock_select:
        mock_select.return_value.execute.return_value = "d. Exit"
        lab5ui.select_dataset_column(pop_df, ["a. Pop Apr 1", "d. Exit"], "Population Data")

    mock_stats.assert_not_called()
    mock_hist.assert_not_called()
    output = capsys.readouterr().out
    assert "Exiting Population Data analysis." in output


@patch("lab5ui.display_histogram")
@patch("lab5ui.compute_statistics")
def test_select_dataset_column_processes_one_column_then_exits(
    mock_stats, mock_hist, pop_df
):
    with patch("lab5ui.inquirer.select") as mock_select:
        mock_select.return_value.execute.side_effect = [
            "a. Pop Apr 1",
            "d. Exit",
        ]
        lab5ui.select_dataset_column(
            pop_df,
            ["a. Pop Apr 1", "b. Pop Jul 1", "c. Change Pop", "d. Exit"],
            "Population Data",
        )

    mock_stats.assert_called_once()
    mock_hist.assert_called_once()


@patch("lab5ui.select_dataset_column")
def test_lab5ui_routes_to_population_data(mock_select_column, pop_df, housing_df):
    with patch("lab5ui.inquirer.select") as mock_select:
        mock_select.return_value.execute.side_effect = [
            "Population Data",
            "Exit",
        ]
        lab5ui.lab5ui(pop_data=pop_df, housing_data=housing_df)

    mock_select_column.assert_called_once()
    kwargs = mock_select_column.call_args.kwargs
    assert kwargs["dataframe"] is pop_df
    assert kwargs["dataset_name"] == "Population Data"


@patch("lab5ui.select_dataset_column")
def test_lab5ui_routes_to_housing_data(mock_select_column, pop_df, housing_df):
    with patch("lab5ui.inquirer.select") as mock_select:
        mock_select.return_value.execute.side_effect = [
            "Housing Data",
            "Exit",
        ]
        lab5ui.lab5ui(pop_data=pop_df, housing_data=housing_df)

    mock_select_column.assert_called_once()
    kwargs = mock_select_column.call_args.kwargs
    assert kwargs["dataframe"] is housing_df
    assert kwargs["dataset_name"] == "Housing Data"


@patch("lab5ui.select_dataset_column")
def test_lab5ui_exits_when_user_selects_exit(mock_select_column, pop_df, housing_df, capsys):
    with patch("lab5ui.inquirer.select") as mock_select:
        mock_select.return_value.execute.return_value = "Exit"
        lab5ui.lab5ui(pop_data=pop_df, housing_data=housing_df)

    mock_select_column.assert_not_called()
    output = capsys.readouterr().out
    assert "Thanks for using the Data Analysis App" in output
