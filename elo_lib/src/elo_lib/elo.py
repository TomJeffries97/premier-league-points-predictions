import requests
import pandas as pd
from datetime import datetime

API_URL = "http://api.clubelo.com"
API_CALL_ATTEMPTS = 1


def call_elo_api(url:str):
    """run a get to the url and return a pd.Dataframe

    :param url: url to query
    :return:
    """
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
    assert response.status_code == 200, "unsuccessful API call"
    ratings = [line.split(",") for line in response.text.split("\n")]
    rating_columns = ratings.pop(0)
    return pd.DataFrame.from_records(ratings, columns=rating_columns)



def get_elo_rating(date: str = None, fallback: str = "./data/fallback_elo_data.csv"):
    """retrieve ELO ratings from the ClubELO API for a given date.

    :param date:
    :param fallback: Path to a fallback CSV file containing ELO ratings if the API call fails.
    :return:
    """
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    for attempt in range(API_CALL_ATTEMPTS):
        # Ive since refactored the code and broken the api call out across two functions which I don't like
        try:
            url = f"{API_URL}/{date}"
            ratings = call_elo_api(url)

        except requests.RequestException as e:
            print(f"Attempt {attempt + 1}: Failed to fetch ELO ratings from API. Error: {e}")
            if attempt == API_CALL_ATTEMPTS - 1:
                print("Using fallback data.")
                ratings = pd.read_csv(fallback)

    assert ["Rank", "Club", "Country", "Level", "Elo", "From", "To"] == list(ratings.columns)

    # clean the dataframe
    ratings = ratings[["Club", "Country", "Level", "Elo"]].dropna()
    ratings["Club"] = ratings["Club"].astype(str)
    ratings["Country"] = ratings["Country"].astype(str)
    ratings["Level"] = ratings["Level"].astype(int)
    ratings["Elo"] = ratings["Elo"].astype(float)

    return ratings




