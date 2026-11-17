CREATE OR REFRESH STREAMING TABLE footballdb.default.bronze_leagues AS 
SELECT *,
_metadata.file_name,
_metadata.file_path,
_metadata.file_modification_time
FROM STREAM read_files(
"/Volumes/footballdb/default/jsonfiles/leagues/",
format => "json",
header => true,
schema => "STRUCT<country_code: STRING, country_flag: STRING, country_name: STRING, league_id: BIGINT, league_logo: STRING, league_name: STRING, league_type: STRING, season_coverage_fixtures_events: BOOLEAN, season_coverage_fixtures_lineups: BOOLEAN, season_coverage_fixtures_statistics_fixtures: BOOLEAN, season_coverage_fixtures_statistics_players: BOOLEAN, season_coverage_injuries: BOOLEAN, season_coverage_odds: BOOLEAN, season_coverage_players: BOOLEAN, season_coverage_predictions: BOOLEAN, season_coverage_stadings: BOOLEAN, season_coverage_top_assists: BOOLEAN, season_coverage_top_cards: BOOLEAN, season_coverage_top_scorers: BOOLEAN, season_current: BOOLEAN, season_end: STRING, season_start: STRING, season_year: BIGINT>",
rescuedDataColumn => "_rescued_data"
) ;


drop table if exists footballdb.default.temp_bronze_leagues;
CREATE TABLE footballdb.default.temp_bronze_leagues AS
select
ifnull(country_code, 'N/A') as country_code,
ifnull(country_flag, 'N/A') as country_flag,
ifnull(country_name, 'N/A') as country_name,
ifnull(league_id, -1) as league_id,
league_logo,
league_name,
league_type,
season_coverage_fixtures_events,
season_coverage_fixtures_lineups,
season_coverage_fixtures_statistics_fixtures,
season_coverage_fixtures_statistics_players,
season_coverage_injuries,
season_coverage_odds,
season_coverage_players,
season_coverage_predictions,
season_coverage_stadings,
season_coverage_top_assists,
season_coverage_top_cards,
season_coverage_top_scorers,
season_current,
season_end,
season_start,
season_year,
file_modification_time updated_at
from footballdb.default.bronze_leagues
qualify row_number() over(partition by league_id, season_year order by file_modification_time desc) = 1;
