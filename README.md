# Sure-Bet Strategy Automatization

Project whose final goal is to automate betting strategies in different betting houses and guaranteeing mathematically a positive profitability by [arbitrage](https://en.wikipedia.org/wiki/Arbitrage). 

Odds are obtained through https://the-odds-api.com/, they are supposed to be real-time odds but in practice they aren´t. I chose this one since it has a free memeber plan.

## Functionality

In Telegram:

1.- Start chat with @raw_data_bot and copy your ID

2.- Paste your ID in line 116 of "odd_api.py"

3.- Start chat with @Betsss14_bot

4.-Execute "odd_api.py"

5.- In your telegram chat with @Betsss14_bot you will see all bets wich profitability is over 1% (can be set to over 0% in code or any other value).



## Problems to finish the project:

1.- Benefits over 3% are rare and last just a short period time. Need of having real-time odds to take advantage of the betting houses errors, which lasts just a few minutes.

2.- No public/free (nor cheap) access to real-time odds from various betting houses. The one I chose (OddsApi) doesn´t provide real-time odds even if they say so (at least on the free plan).

3.- Unable to have a real-time system based on scrapping various betting houses as the scrapping process is really slow (done on purpose by betting houses to protect themselves). Just to scrap 'LaLiga' from Betfair took 10 seconds, imposible to scrap every league from every betting house in 'real-time' (not even in 1 minute).


If I had access to real-time odds I would finish this project and  automate the betting process on each betting house.
