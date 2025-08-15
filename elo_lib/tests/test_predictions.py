import pytest
import pandas as pd

from elo_lib.predict import predict_points


def test_predict_points_league_name():
    """very simple test to predict points for each team based on ELO ratings and fixtures.
    No mock data is used, so this is an end to end test, very basic and needs to be split up

    :return:
    """
    # Predict points for each team based on ELO ratings and fixtures
    predictions = predict_points(date="2025-08-12", league="premier league")

    # Check if the predictions DataFrame is not empty
    assert isinstance(predictions, pd.DataFrame), "Expected a DataFrame"
    assert not predictions.empty, "Predictions DataFrame should not be empty"

    # Check if the expected columns are present
    expected_columns = ["team", "expected_total_points"]
    assert all(col in predictions.columns for col in expected_columns), f"Expected columns {expected_columns} not found in predictions DataFrame"

    # Check if the DataFrame has the correct number of rows (teams)
    assert len(predictions) > 0, "Predictions DataFrame should have more than 0 rows"


def test_predict_points_none():
    """very simple test to predict points for each team based on ELO ratings and fixtures with none as the league.
    No mock data is used, so this is an end to end test, very basic and needs to be split up.
    by using none it should defailt to the input csv

    :return:
    """
    # Predict points for each team based on ELO ratings and fixtures
    predictions = predict_points(date="2025-08-12")

    # Check if the predictions DataFrame is not empty
    assert isinstance(predictions, pd.DataFrame), "Expected a DataFrame"
    assert not predictions.empty, "Predictions DataFrame should not be empty"

    # Check if the expected columns are present
    expected_columns = ["team", "expected_total_points"]
    assert all(col in predictions.columns for col in expected_columns), f"Expected columns {expected_columns} not found in predictions DataFrame"

    # Check if the DataFrame has the correct number of rows (teams)
    assert len(predictions) > 0, "Predictions DataFrame should have more than 0 rows"