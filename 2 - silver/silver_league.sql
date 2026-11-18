/*
FIRST OF ALL, TABLE WAS CREATE USING THE FOLLOWING COMMAND. AFTERWARDS, IT WAS PERFORMED THE ALTER COLUMN COMMAND TO SET NOT NULL TO THE COLUMN season_year AND league_id.

CREATE TABLE footballdb.default.silver_leagues AS
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

ALTER TABLE footballdb.default.silver_leagues ALTER COLUMN season_year SET NOT NULL;
ALTER TABLE footballdb.default.silver_leagues ALTER COLUMN league_id SET NOT NULL;
*/


MERGE INTO footballdb.default.silver_leagues t
USING (
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
    qualify row_number() over(partition by league_id, season_year order by file_modification_time desc) = 1
) AS s
ON t.league_id = s.league_id AND t.season_year = s.season_year
WHEN MATCHED THEN
UPDATE SET *
WHEN NOT MATCHED
THEN INSERT *
;

