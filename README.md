# premier-league-points-predictions
A simple library to call ELO Api to retrieve ratings for a list of football teams, generate a fixture list and create an end-of-season point prediction for each team. 

## Installation
To install the library, from the base of the repo run:
```bash 
pip install elo_lib/src
```

## How to run
The main.py file contains a simple example of how to use the library.
Comment out the lines to try different combinations 

To run pytests, simply run:
```bash
pip install -r elo_lib/src/requirements-dev.txt
python -m pytest elo_lib/src/tests
```

## Design choice
I chose to create a library for this core component so that it is easily deployable into any system.
This does mean that it remains isolated from other components, so ideally it would be integrated into other libraries 
that are being used in the desired orchestrators which is running the etl. 

I used pandas as the main workhorse for the data cleaning and manipulation. This is for ease of development and 
accessibility to the library for any data engineer or data scientist.

## Key assumptions
- Assumed that the orchestrator that will be used for the pipeline/ wider functionality can install custom packages.
- Assumed that this package will be picked up by a 'python engineer' to deploy it
- Someone might want to change the fallback and input files easily, so they have been left as the default values to the 
functions and nothing more - a design decision I question


## Additional features 
Extended the library to operate for the top 5 leagues in europe, predicting results for:
- Premier League
- La Liga
- Bundesliga
- Ligue 1
- Serie A

This was implemented with the use of Enums to validate the user's league entry, and then to allign the league 
to the correct country code. For this small use case, this might have been overkill, however it was done with future 
expansion in mind, creating a framework for input validation. 

This could be done using the ELO api response. Therefore the code has been expanded to allow for either a csv input of 
teams to play in that league (an example csv has been created in the data/inputs directory) or by entering the name of 
one of the top 5 leagues.

The function expects a string variable called 'league' which can be a csv path (found by if '.csv' in league) or a 
string of the league name (e.g. 'Premier League', 'La Liga', etc.).

Key assumption: The CSV input of the league's teams will be a csv with a column called 'Club'.


Note: This only works for the top 5 leagues as they currently stand (it uses the current date to determine ELO scores 
and such the country and league tier of the team)

## Next Steps
In the short term:
- Increase the range and scope of unit testing (limited could be written in the 3 hours)
- Increase the depth of unit/integration testing. For now some are end to end tests, which will be prone to fail. I have
began the process of mocking data but this has not been implemented
- Improve error catching and handling (specifically focused on the api calls and CSV inputs)
- Clean up the library and its setup (move to pytoml for example). I went for the a slightly outdated setup of a library
using setup.py and requirements.txt, however this is not the most modern way of doing things. This was done as I have 
more experience with this and could move forward quicker in the 3 hour slot. 

Moving forward:
- Integrate cloud storage to the solution (save ELO files and league files to storage to reduce dependency on api)
- Stream solution to some kind of database (BigQuery, Snowflake for example)
- deploy into wider system
- intregrate CI/CD, with GitHub actions or similar to run tests and deploy the library.

## Bugs/percularities in code
- The default value for league and fallback doesn't quite carry through, meaning I have had to define the default twice
as a quick fix.