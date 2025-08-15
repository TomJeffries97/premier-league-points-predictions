import pytest
import pandas as pd

from elo_lib.fixtures import generate_fixtures, get_clubs


@pytest.fixture
def sample_clubs_df():
    """Fixture to provide a sample DataFrame of clubs."""
    return pd.DataFrame({
        "Club": ["TeamA", "TeamB", "TeamC", "TeamD"],
        "Country": ["ENG", "ENG", "ENG", "ENG"],
        "Level": [1, 1, 1, 1],
        "Elo": [1500, 1600, 1550, 1400]
    })


def test_correct_number_of_fixtures(sample_clubs_df):
    """Test that the correct number of fixtures are generated."""
    num_clubs = len(sample_clubs_df)
    expected_count = num_clubs * (num_clubs - 1)  # Each team plays every other team twice

    fixtures_df = generate_fixtures(sample_clubs_df)

    assert len(fixtures_df) == expected_count
    assert list(fixtures_df.columns) == ["home_team", "away_team"]


def test_get_clubs_csv():
    """Test that get_clubs returns clubs from a CSV file.
    requires a csv file at data/input/premier_league.csv

    :return:
    """
    clubs = get_clubs("data/input/premier_league.csv")
    assert isinstance(clubs, pd.DataFrame), "Expected a DataFrame"
    assert "Club" in clubs.columns, "Expected 'Club' column in DataFrame"
    assert clubs.shape[0] > 0, "Expected non-empty DataFrame"
    assert not clubs.empty, "API call returned an empty DataFrame"


def test_get_clubs_league_name():
    """
    Test that get_clubs returns clubs based on league name, using the ELO api
    :return:
    """
    clubs = get_clubs("premier league")
    assert isinstance(clubs, pd.DataFrame), "Expected a DataFrame"
    assert "Club" in clubs.columns, "Expected 'Club' column in DataFrame"
    assert clubs.shape[0] > 0, "Expected non-empty DataFrame"
    assert not clubs.empty, "API call returned an empty DataFrame"
