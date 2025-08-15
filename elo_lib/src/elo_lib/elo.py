import requests
import pandas as pd
from datetime import datetime

API_URL = "http://api.clubelo.com"
API_CALL_ATTEMPTS = 1


def get_elo_rating(date: str = None, fallback: str = "./data/fallback_elo_data.csv"):
    """retrieve ELO ratings from the ClubELO API for a given date.

    :param date:
    :param fallback: Path to a fallback CSV file containing ELO ratings if the API call fails.
    :return:
    """
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')

    for attempt in range(API_CALL_ATTEMPTS):
        try:
            response = requests.get(f"{API_URL}/{date}")
            assert response.status_code == 200, "unsuccessful API call"
            ratings = [line.split(",") for line in response.text.split("\n")]
            rating_columns = ratings.pop(0)
            ratings = pd.DataFrame.from_records(ratings, columns=rating_columns)

        except requests.RequestException as e:
            print(f"Attempt {attempt + 1}: Failed to fetch ELO ratings from API. Error: {e}")
            if attempt == API_CALL_ATTEMPTS - 1:
                print("Using fallback data.")
                ratings = pd.read_csv(fallback)

    assert ['Rank', 'Club', 'Country', 'Level', 'Elo', 'From', 'To'] == list(ratings.columns)

    # clean the dataframe
    ratings = ratings[['Club', 'Country', 'Level', 'Elo']].dropna()
    ratings['Club'] = ratings['Club'].astype(str)
    ratings['Country'] = ratings['Country'].astype(str)
    ratings['Level'] = ratings['Level'].astype(int)
    ratings['Elo'] = ratings['Elo'].astype(float)

    return ratings




if __name__ == '__main__':
    get_elo_rating()



