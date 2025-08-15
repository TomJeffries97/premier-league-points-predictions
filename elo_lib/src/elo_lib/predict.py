from elo_lib.elo import get_elo_rating
from elo_lib.fixtures import generate_fixtures, get_clubs


def predict_points(date: str = None, league: str = None, fallback: str = None):
    """
    Predict points for each team based on ELO ratings and fixtures.

    :return: DataFrame with predicted points for each team
    """
    # Get clubs and fixtures
    clubs = get_clubs(league=league)
    fixtures = generate_fixtures(clubs)

    # Get ELO ratings
    elo_ratings = get_elo_rating(date=date, fallback=fallback)

    # Merge clubs with ELO ratings
    ratings = clubs.merge(elo_ratings, how='left', on='Club')[['Club','Elo']]

    # Merge fixtures with ELO ratings
    fixtures = fixtures.merge(ratings, how='left', left_on='home_team', right_on='Club')[['home_team', 'away_team' , 'Elo']].rename(columns={'Elo':'home_rating'})
    fixtures = fixtures.merge(ratings, how='left', left_on='away_team', right_on='Club')[['home_team', 'away_team', 'home_rating', 'Elo']].rename(columns={'Elo':'away_rating'})

    # Calculate home pediction to win
    fixtures['home_win_prob'] = 1/(1+10**(-(fixtures['home_rating']+100-fixtures['away_rating'])/400))
    fixtures['away_win_prob'] = 1 - fixtures['home_win_prob']

    # Calculate expected points per game
    fixtures['expected_home_points'] = fixtures['home_win_prob'] * 3
    fixtures['expected_away_points'] = fixtures['away_win_prob'] * 3

    # group by each football team home and away
    home_points = fixtures[['home_team', 'expected_home_points']].groupby(['home_team']).sum().reset_index()\
        .rename(columns={'home_team':'team'})
    away_points = fixtures[['away_team', 'expected_away_points']].groupby(['away_team']).sum().reset_index()\
        .rename(columns={'away_team':'team'})

    # find total points for each club
    total_points = home_points.merge(away_points, how='left', on='team')
    total_points['expected_total_points'] = total_points['expected_home_points'] + total_points['expected_away_points']

    return total_points[['team', 'expected_total_points']].sort_values(by=['expected_total_points'], ascending=False)
