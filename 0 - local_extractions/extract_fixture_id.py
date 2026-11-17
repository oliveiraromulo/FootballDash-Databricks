import requests
import json
#import argparse
#import config
from datetime import datetime
import psycopg as pg # pyright: ignore[reportMissingImports]
import sys, os
sys.path.append(os.path.abspath("/home/romulo/Documents/Git/PaineldoFutebol/Databricks/utils"))
from auxiliar_functions import upload_file_to_volume, get_api_credentials, get_databricks_credentials
import os
from databricks import sql
'''
    Reading configuration files and setting headers for API requests and databases
'''
args = get_api_credentials('dev') # or 'dev' depending on the environment
args_databricks = get_databricks_credentials('dev') # or 'dev' depending on the environment

headers = {
    'x-apisports-key': args['x-apisports-key']
    }

url = "https://v3.football.api-sports.io/leagues"


send_db = False # Set to True if you want to send the data to the database, False otherwise

def extract_fixture_id(url, headers, querystring) -> list:
    response = requests.request("GET", url, headers=headers, params=querystring)
    json_data = json.loads(response.text)

    results = []

    for fixture in json_data['response']:
        fixture_id = fixture['fixture']['id']
        fixture_referee = fixture['fixture']['referee']
        fixture_timezone = fixture['fixture']['timezone']
        fixture_date = fixture['fixture']['date']
        fixture_timestamp = fixture['fixture']['timestamp']
        fixture_period_first = fixture['fixture']['periods']['first']
        fixture_period_second = fixture['fixture']['periods']['second']
        fixture_venue_id = fixture['fixture']['venue']["id"]
        fixture_venue_name = fixture['fixture']['venue']["name"]
        fixture_venue_city = fixture['fixture']['venue']["city"]
        fixture_status_long = fixture['fixture']['status']["long"]
        fixture_status_short = fixture['fixture']['status']["short"]
        fixture_status_elapsed = fixture['fixture']['status']["elapsed"]

        league_id = fixture['league']['id']
        league_name = fixture['league']['name']
        league_country = fixture['league']['country']
        league_logo = fixture['league']['logo']
        league_flag = fixture['league']['flag']
        league_season = fixture['league']['season']
        league_round = fixture['league']['round']

        teams_home_id = fixture['teams']['home']['id']
        teams_home_name = fixture['teams']['home']['name']
        teams_home_logo = fixture['teams']['home']['logo']
        teams_home_winner = fixture['teams']['home']['winner']
        teams_away_id = fixture['teams']['away']['id']
        teams_away_name = fixture['teams']['away']['name']
        teams_away_logo = fixture['teams']['away']['logo']
        teams_away_winner = fixture['teams']['away']['winner']

        goals_home =  fixture['goals']['home']
        goals_away = fixture['goals']['away']

        score_halftime_home = fixture['score']['halftime']['home']
        score_halftime_away = fixture['score']['halftime']['away']
        score_fulltime_home = fixture['score']['fulltime']['home']
        score_fulltime_away = fixture['score']['fulltime']['away']
        score_extratime_home = fixture['score']['extratime']['home']
        score_extratime_away = fixture['score']['extratime']['away']
        score_penalty_home = fixture['score']['penalty']['home']
        score_penalty_away = fixture['score']['penalty']['away']

        json_fixture_id = {
            "fixture_id": fixture_id,
            "fixture_referee": fixture_referee,
            "fixture_timezone": fixture_timezone,
            "fixture_date": fixture_date,
            "fixture_timestamp": fixture_timestamp,
            "fixture_period_first": fixture_period_first,
            "fixture_period_second": fixture_period_second,
            "fixture_venue_id": fixture_venue_id,
            "fixture_venue_name": fixture_venue_name,
            "fixture_venue_city": fixture_venue_city,
            "fixture_status_long": fixture_status_long,
            "fixture_status_short": fixture_status_short,
            "fixture_status_elapsed": fixture_status_elapsed,
            "league_id": league_id,
            "league_name": league_name,
            "league_country": league_country,
            "league_logo": league_logo,
            "league_flag": league_flag,
            "league_season": league_season,
            "league_round": league_round,
            "teams_home_id": teams_home_id,
            "teams_home_name": teams_home_name,
            "teams_home_logo": teams_home_logo,
            "teams_home_winner": teams_home_winner,
            "teams_away_id": teams_away_id,
            "teams_away_name": teams_away_name,
            "teams_away_logo": teams_away_logo,
            "teams_away_winner": teams_away_winner,
            "goals_home": goals_home,
            "goals_away": goals_away,
            "score_halftime_home": score_halftime_home,
            "score_halftime_away": score_halftime_away,
            "score_fulltime_home": score_fulltime_home,
            "score_fulltime_away": score_fulltime_away
        }

        # For each fixture, print the JSON data to the console for debugging purposes. Also send the JSON data to a file in the Databricks volume for further processing.

        print(json_fixture_id)
    
        filename = "fixture_id_{}_{}.json".format(fixture_id, datetime.now().strftime("%Y%m%d_%H%M%S"))

        local_path = "/home/romulo/Documents/Git/PaineldoFutebol/Databricks/utils/"
        
        with open(f"{local_path}{filename}", "w") as json_file:
            json.dump(json_fixture_id, json_file)
    
        upload_file_to_volume(#local_file_path=f"/opt/airflow/{filename}",
                                local_file_path=f"{local_path}{filename}",
                                catalog='footballdb',
                                volume='jsonfiles',
                                folder='fixtures',
                                filename=filename)

        results.append((
        fixture_id,
        fixture_referee,
        fixture_timezone,
        fixture_date,
        fixture_timestamp,
        fixture_period_first,
        fixture_period_second,
        fixture_venue_id,
        fixture_venue_name,
        fixture_venue_city,
        fixture_status_long,
        fixture_status_short,
        fixture_status_elapsed,
        league_id,
        league_name,
        league_country,
        league_logo,
        league_flag,
        league_season,
        league_round,
        teams_home_id,
        teams_home_name,
        teams_home_logo,
        teams_home_winner,
        teams_away_id,
        teams_away_name,
        teams_away_logo,
        teams_away_winner,
        goals_home,
        goals_away,
        score_halftime_home,
        score_halftime_away,
        score_fulltime_home,
        score_fulltime_away,
        score_extratime_home,
        score_extratime_away,
        score_penalty_home,
        score_penalty_away))

    return results


with sql.connect(server_hostname = args_databricks['warehouse_server'], 
                 http_path = args_databricks['warehouse_http_path'], 
                 access_token = args_databricks['token']) as connection:

  with connection.cursor() as cursor:
    cursor.execute("""select distinct league_id,
                                      country_name, season_year 
                    from footballdb.default.silver_leagues""")
    leagues = cursor.fetchall()


    for league in leagues:
        querystring = {
            #"date":"2021-11-16",
            "league": f"{league[0]}",
            "season": f"{league[2]}"
        }

        print("Extracting fixtures from : ", league[1], " and season: ", league[2])

        print(querystring)

        fixtures = extract_fixture_id(url, headers, querystring)

        '''
            Sending files to Databricks volume
        '''
        # filename = "fixtures_id_{}.json".format(datetime.now().strftime("%Y%m%d_%H%M%S"))

        # local_path = "/home/romulo/Documents/Git/PaineldoFutebol/Databricks/utils/"
            
        # with open(f"{local_path}{filename}", "w") as json_file:
        #     json.dump(fixtures, json_file)

        # print("Listing files in local before sending to Databricks volume: ", os.listdir("/opt/airflow/"))

        # upload_file_to_volume(local_file_path=f"/opt/airflow/{filename}",
        #                         catalog='footballdb',
        #                         volume='jsonfiles',
        #                         folder='fixtures',
        #                         filename=filename)
