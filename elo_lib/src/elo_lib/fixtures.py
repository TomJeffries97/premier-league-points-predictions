import pandas as pd
from enum import Enum

from .elo import get_elo_rating



class Leagues(Enum):
    PREMIER_LEAGUE = "premier league"
    BUNDESLIGA = "bundesliga"
    LA_LIGA = "la liga"
    SERIE_A = "serie a"
    LIGUE_1 = "ligue 1"


class Country(Enum):
    ENG = 'ENG'
    FRA = 'FRA'
    ESP = 'ESP'
    GER = 'GER'
    ITA = 'ITA'


LEAGUE_COUNTRY_MAP = {
    Leagues.PREMIER_LEAGUE: Country.ENG,
    Leagues.BUNDESLIGA: Country.GER,
    Leagues.LA_LIGA: Country.ESP,
    Leagues.SERIE_A: Country.ITA,
    Leagues.LIGUE_1: Country.FRA
}

def get_clubs(league: str = 'data/input/premier_league.csv', league_is_path_flag: bool = True):
    """
    Get the clubs provided my input CSV of the single column schema {Club: string} or by calling a league by name

    :return: Dataframe of clubs
    """
    if '.csv' in league:
        clubs = pd.read_csv(league)
    else:
        league = league.lower()
        assert league in [league.value for league in Leagues], "unknown league"
        league = Leagues(league)
        country = LEAGUE_COUNTRY_MAP[league]
        elo = get_elo_rating()
        clubs = elo[(elo['Level'] == 1) & (elo['Country'] == country.value)]
        assert clubs.shape[0] > 0, "returning an empty dataframe"

    clubs = clubs['Club']
    return clubs.reset_index()


def generate_fixtures(clubs: pd.DataFrame):
    """
    Generate fixtures for the given clubs. Each team will play the other team twice, once at home and once away.

    :param clubs:
    :return: Dataframe of fixtures with columns [home_team, away_team, home_team_id, away_team_id]
    """
    fixtures = []
    for i in range(len(clubs)):
        for j in range(i+1, len(clubs)):
            # append first fixture
            fixtures.append({
                'home_team': clubs.iloc[i]['Club'],
                'away_team': clubs.iloc[j]['Club'],
            })
            # append the reverse fixture
            fixtures.append({
                'home_team': clubs.iloc[j]['Club'],
                'away_team': clubs.iloc[i]['Club'],
            })
    assert len(fixtures) == (len(clubs) - 1) * len(clubs), "Fixtures count mismatch: Expected twice the number of matches"
    return pd.DataFrame(fixtures)


