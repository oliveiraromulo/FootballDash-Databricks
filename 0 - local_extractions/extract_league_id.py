import requests
import json
from datetime import datetime

import sys, os
sys.path.append(os.path.abspath("/home/romulo/Documents/Git/FootballDash - Databricks/utils"))
from auxiliar_functions import upload_file_to_volume, get_api_credentials

'''
    Reading configuration files and setting headers for API requests and databases
'''
args = get_api_credentials('dev') # 'prd' or 'dev' depending on the environment

headers = {
    'x-apisports-key': args['x-apisports-key']
    }

url = "https://v3.football.api-sports.io/leagues"

extract_league_id = [1, 71]

def extract_league_ids(url : str, headers : dict) -> list:
    results = []
    
    response = requests.request("GET", url, headers=headers)
    json_data = json.loads(response.text)

    for league in json_data['response']:
        if league["league"]["id"] in extract_league_id:
            txt = "ID: {} - Nome: {} - {} | Temporadas: {}".format(league["league"]["id"], 
                                                                   league["country"]["name"],
                                                                   league["league"]["name"],
                                                                   len(league["seasons"])
                                                                )
            print(txt)

            league_id = league["league"]["id"]
            league_name = league["league"]["name"]
            league_type = league["league"]["type"]
            league_logo = league["league"]["logo"]
            country_name = league["country"]["name"]
            country_code = league["country"]["code"]
            country_flag = league["country"]["flag"]
            season_qtd = len(league["seasons"])

            for j in range(1, season_qtd):
                season_year = league["seasons"][j]["year"]
                season_start = league["seasons"][j]["start"]
                season_end = league["seasons"][j]["end"]
                season_current = league["seasons"][j]["current"]
                season_coverage_fixtures_events = league["seasons"][j]["coverage"]["fixtures"]["events"]
                season_coverage_fixtures_lineups = league["seasons"][j]["coverage"]["fixtures"]["lineups"]
                season_coverage_fixtures_statistics_fixtures = league["seasons"][j]["coverage"]["fixtures"]["statistics_fixtures"]
                season_coverage_fixtures_statistics_players = league["seasons"][j]["coverage"]["fixtures"]["statistics_players"]
                season_coverage_stadings = league["seasons"][j]["coverage"]["standings"]
                season_coverage_players = league["seasons"][j]["coverage"]["players"]
                season_coverage_top_scorers = league["seasons"][j]["coverage"]["top_scorers"]
                season_coverage_top_assists = league["seasons"][j]["coverage"]["top_assists"]
                season_coverage_top_cards = league["seasons"][j]["coverage"]["top_cards"]
                season_coverage_injuries = league["seasons"][j]["coverage"]["injuries"]
                season_coverage_predictions = league["seasons"][j]["coverage"]["predictions"]
                season_coverage_odds = league["seasons"][j]["coverage"]["odds"]

                json_league = {
                    "league_id": league_id, 
                    "league_name": league_name, 
                    "league_type": league_type, 
                    "league_logo": league_logo, 
                    "country_name": country_name, 
                    "country_code": country_code,
                    "country_flag": country_flag,
                    "season_year": season_year,
                    "season_start": season_start,
                    "season_end": season_end,
                    "season_current": season_current,
                    "season_coverage_fixtures_events": season_coverage_fixtures_events,
                    "season_coverage_fixtures_lineups": season_coverage_fixtures_lineups,
                    "season_coverage_fixtures_statistics_fixtures": season_coverage_fixtures_statistics_fixtures,
                    "season_coverage_fixtures_statistics_players": season_coverage_fixtures_statistics_players,
                    "season_coverage_stadings": season_coverage_stadings,
                    "season_coverage_players": season_coverage_players,
                    "season_coverage_top_scorers": season_coverage_top_scorers,
                    "season_coverage_top_assists": season_coverage_top_assists,
                    "season_coverage_top_cards": season_coverage_top_cards,
                    "season_coverage_injuries": season_coverage_injuries,
                    "season_coverage_predictions": season_coverage_predictions,
                    "season_coverage_odds": season_coverage_odds
                }

                print(json_league)
            
                filename = "league_id_{}_{}_{}.json".format(league_id, season_year, datetime.now().strftime("%Y%m%d_%H%M%S"))

                local_path = "/home/romulo/Documents/Git/PaineldoFutebol/Databricks/utils/"
                
                with open(f"{local_path}{filename}", "w") as json_file:
                    json.dump(json_league, json_file)
            
                upload_file_to_volume(#local_file_path=f"/opt/airflow/{filename}",
                                    local_file_path=f"{local_path}{filename}",
                                        catalog='footballdb',
                                        volume='jsonfiles',
                                        folder='leagues',
                                        filename=filename)

'''
    Only execute the extraction and load new league ids on the first day of each month
    since this data doesn't change frequently.
'''

if datetime.now().day in [17]:
    extract_league_ids(url, headers)
