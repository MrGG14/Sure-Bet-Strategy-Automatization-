# -*- coding: utf-8 -*-

"""
Created on Tue Oct  4 20:28:38 2022

@author: Nico
"""

import requests as re
import pandas as pd
import json

pd.options.mode.chained_assignment = None
key = 'f8bf74f20a2de6a7c8ab3eaf8a52b312'

'''
Regions: us/uk/au/eu
Markets: h2h/totals
'''


def sport_odds(sport, region='eu', markets='h2h', key='f8bf74f20a2de6a7c8ab3eaf8a52b312'):
    api_resp = re.get(f'https://api.the-odds-api.com/v4/sports/{sport}/odds',
                      params={
                          'api_key': key,
                          'regions': region,
                          'markets': markets
                      })
    if api_resp.status_code != 200:
        print(f'Failed to get sports: status_code {api_resp.status_code}, response body {api_resp.text}')

    sport_odds_jason = json.dumps(api_resp.json())
    df = pd.read_json(sport_odds_jason)

    if df.empty:
        return None

    odds1 = []
    draw_odds = []
    odds2 = []
    all_rents = []
    all_match_odds = df['bookmakers']

    for match_odds in all_match_odds:
        max1 = 0
        max_draw = 0
        max2 = 0
        for bookmaker_odd in match_odds:
            odd1 = (
            bookmaker_odd['markets'][0]['outcomes'][0]['name'], bookmaker_odd['markets'][0]['outcomes'][0]['price'],
            bookmaker_odd['title'])
            odd2 = (
            bookmaker_odd['markets'][0]['outcomes'][1]['name'], bookmaker_odd['markets'][0]['outcomes'][1]['price'],
            bookmaker_odd['title'])
            draw_odd = (
            bookmaker_odd['markets'][0]['outcomes'][2]['name'], bookmaker_odd['markets'][0]['outcomes'][2]['price'],
            bookmaker_odd['title'])

            if odd1[1] > max1:
                max1 = odd1[1]
                best1 = odd1

            if draw_odd[1] > max_draw:
                max_draw = draw_odd[1]
                best_draw = draw_odd

            if odd2[1] > max2:
                max2 = odd2[1]
                best2 = odd2

        odds1.append(best1)
        draw_odds.append(best_draw)
        odds2.append(best2)

        euros_min = (1 / max1) + (1 / max_draw) + (1 / max2)
        all_rents.append((1 - euros_min) * 100)

    df['max_odd1'] = odds1
    df['max_draw'] = draw_odds
    df['max_odd2'] = odds2
    df['rentabilidad(%)'] = all_rents

    # no interesan beneficios menores a 1%
    sure_df = df[df['rentabilidad(%)'] > 1]
    sure_df['min1'] = 1 / sure_df['max_odd1'].map(lambda x: x[1])
    sure_df['min_empate'] = 1 / sure_df['max_draw'].map(lambda x: x[1])
    sure_df['min2'] = 1 / sure_df['max_odd2'].map(lambda x: x[1])
    sure_df.drop(columns=['id', 'commence_time', 'sport_title', 'bookmakers'], inplace=True)
    sure_df.sort_values(by='rentabilidad(%)', axis=0, ascending=False, inplace=True)
    return sure_df


def full_odds_df(leagues):
    df = pd.DataFrame()
    for league in leagues:
        odds = sport_odds(league)
        df = pd.concat([df, odds], ignore_index=True)
    df.sort_values(by='rentabilidad(%)', axis=0, ascending=False, inplace=True)
    return df


def main():
    leagues = ['soccer_spain_la_liga', 'soccer_fifa_world_cup', 'soccer_australia_aleague', 'soccer_belgium_first_div',
               'soccer_england_efl_cup', 'soccer_england_league1', 'soccer_england_league2', 'soccer_epl',
               'soccer_france_ligue_one', 'soccer_germany_bundesliga', 'soccer_germany_bundesliga2',
               'soccer_italy_serie_a', 'soccer_italy_serie_b', 'soccer_netherlands_eredivisie',
               'soccer_poland_ekstraklasa', 'soccer_portugal_primeira_liga', 'soccer_spain_segunda_division',
               'soccer_spl', 'soccer_uefa_champs_league', 'soccer_uefa_europa_conference_league',
               'soccer_uefa_europa_league']
    odds_df = full_odds_df(leagues)

    token = '5663636493:AAHa2IcnhorAfzCFayWLpMYkDULZR5A322U'
    url = f"https://api.telegram.org/bot{token}"

    #obtain your id with @raw_data_bot
    telegram_id = "your id here"

    msgs = []
    for sure_match in odds_df.iterrows():
        local = str(sure_match[1]['home_team'])
        visit = str(sure_match[1]['away_team'])
        odd1 = str(sure_match[1]['max_odd1'])
        odd_draw = str(sure_match[1]['max_draw'])
        odd2 = str(sure_match[1]['max_odd2'])

        rent = str(sure_match[1]['rentabilidad(%)'])[0:4]
        msg = f"{local} - {visit} \n 1: {odd1}  \n X: {odd_draw} \n 2: {odd2} \n Rentabilidad = {rent}%"
        msgs.append(msg)
    for surebet in msgs:
        params = {"chat_id": str(telegram_id), "text": surebet}
        re.get(url + "/sendMessage", params=params)


if __name__ == "__main__":
    main()
