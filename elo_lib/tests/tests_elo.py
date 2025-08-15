import pytest
import pandas as pd

from elo_lib import elo


@pytest.fixture
def mock_data():
    api_success_data = (
        "Rank,Club,Country,Level,Elo,From,To\n"
        "1,Liverpool,ENG,1,2000.0,2023-01-01,2023-12-31\n"
        "2,Man City,ENG,1,2000.0,2023-01-01,2023-12-31\n"
        "3,Real Madrid,ESP,1,1950.0,2023-01-01,2023-12-31\n"
        "4,Bayern Munich,GER,1,1900.0,2023-01-01,2023-12-31\n"
        "4,NoneClub,FRA,2,1800.0,2023-01-01,2023-12-31\n" # Added one with level 2
        "5,MissingElo,ENG,1,,2023-01-01,2023-12-31\n" # Missing Elo value
    )
    fallback_data = pd.DataFrame({
        "Rank": [1, 2, 3],
        "Club": ["Liverpool", "Man City", "Arsenal"],
        "Country": ["ENG", "ENG", "ENG"],
        "Level": [1, 1, 1],
        "Elo": [1850.5, 1840.0, 1830.0],
        "From": ["2022-01-01", "2022-01-01", "2022-01-01"],
        "To": ["2022-12-31", "2022-12-31", "2022-12-31"]
    })
    fallback_csv_path = "./data/test_fallback_elo_data.csv"
    return {
        "api_success_data": api_success_data,
        "fallback_data": fallback_data,
        "fallback_csv_path": fallback_csv_path
    }


def test_call_elo_api():
    """Simple test to ensure the API call returns

    :return: None
    """
    test_url = "http://api.clubelo.com/2025-08-01"
    df = elo.call_elo_api(test_url)
    assert isinstance(df, pd.DataFrame), "API call did not return a DataFrame"
    assert not df.empty, "API call returned an empty DataFrame"
    assert df.shape[0] > 0, "API call returned a DataFrame with no rows"
    for column in ["Rank", "Club", "Country", "Level", "Elo", "From", "To"]:
        assert column in df.columns, f"Missing expected column: {column}"