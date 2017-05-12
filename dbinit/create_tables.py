import psycopg2

def create_stg1_boxscore(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stg1_boxscore(
            game_id CHAR(10),
            team_id CHAR(10),
            team_abbreviation CHAR(3),
            team_city CHAR(32),
            player_id INT,
            player_name CHAR(64),
            start_position CHAR(1),
            comment CHAR(64),
            min CHAR(5),
            fgm INT,
            fga INT,
            fg_pct REAL,
            fg3m INT,
            fg3a INT,
            fg3_pct REAL,
            ftm INT,
            fta INT,
            ft_pct REAL,
            oreb INT,
            dreb INT,
            reb INT,
            ast INT,
            stl INT,
            blk INT,
            tov INT,
            pf INT,
            pts INT,
            plus_minus INT,
            PRIMARY KEY (game_id, player_id))
    """)

def create_stg1_loaded(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stg1_loaded(
            file_name CHAR(32) PRIMARY KEY)
    """)

def create_stg2_season(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stg2_season(
            season_id SERIAL PRIMARY KEY,
            season_type_code INT,
            season_type_descr CHAR(64),
            season_year INT)
    """)

def create_stg2_game_result(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stg2_game_result(
            game_id CHAR(10) PRIMARY KEY,
            winner_team_id CHAR(10),
            winner_pts INT,
            loser_team_id CHAR(10),
            loser_pts INT)
    """)

def create_stg2_season_result(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stg2_season_result(
            team_id CHAR(10),
            season_type CHAR(3),
            season_year CHAR(2),
            win_count INT,
            loss_count INT,
            PRIMARY KEY (season_type, season_year, team_id))
    """)

conn = psycopg2.connect("dbname='nba' user='nba' host='localhost'")
cur = conn.cursor()

create_stg1_boxscore(cur)
create_stg1_loaded(cur)
create_stg2_game_result(cur)
create_stg2_season(cur)
create_stg2_season_result(cur)
conn.commit()

cur.close()
conn.close()