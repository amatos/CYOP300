import pandas as pd
import pytest
from unittest.mock import patch

import main as main_module


@patch("main.lab5ui.lab5ui")
@patch("main.load_csv")
def test_main_loads_both_csv_files(mock_load_csv, mock_ui):
    mock_load_csv.side_effect = [pd.DataFrame({"a": [1]}), pd.DataFrame({"b": [2]})]

    main_module.main()

    assert mock_load_csv.call_count == 2
    called_files = [call.args[0] for call in mock_load_csv.call_args_list]
    assert "Housing.csv" in called_files
    assert "PopChange.csv" in called_files
    mock_ui.assert_called_once()


@patch("main.lab5ui.lab5ui")
@patch("main.load_csv")
def test_main_passes_dataframes_to_ui(mock_load_csv, mock_ui):
    housing_df = pd.DataFrame({"AGE": [10]})
    pop_df = pd.DataFrame({"Pop Apr 1": [100]})
    mock_load_csv.side_effect = [housing_df, pop_df]

    main_module.main()

    mock_ui.assert_called_once_with(pop_data=pop_df, housing_data=housing_df)


@patch("main.load_csv", side_effect=FileNotFoundError)
def test_main_exits_with_code_1_when_file_missing(mock_load_csv):
    with pytest.raises(SystemExit) as exc_info:
        main_module.main()

    assert exc_info.value.code == 1


@patch("main.load_csv", side_effect=FileNotFoundError)
def test_main_prints_missing_file_message(mock_load_csv, capsys):
    with pytest.raises(SystemExit):
        main_module.main()

    output = capsys.readouterr().out
    assert "Housing.csv" in output
    assert "PopChange.csv" in output
