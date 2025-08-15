from elo_lib.predict import predict_points


def main():
    """
    demo function to predict points for each team based on ELO ratings and fixtures.
    """
    # Set date
    date = None
    date = '2025-08-12'
    # Set league
    league = None
    league = 'premier league'
    # set fallback path
    fallback = None

    # Predict points for each team based on ELO ratings and fixtures
    predictions = predict_points(date=date,league=league,fallback=fallback)

    # Print the predictions
    print(predictions)



if __name__ == '__main__':
    main()