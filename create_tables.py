import psycopg2

def create_boxscore(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS boxscore(
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

def create_loaded(cur):
      cur.execute("""
          CREATE TABLE IF NOT EXISTS LOADED(
              file_name CHAR(32) PRIMARY KEY)
          """)

conn = psycopg2.connect("dbname='nba' user='nba' host='localhost'")
cur = conn.cursor()

create_boxscore(cur)
create_loaded(cur)
conn.commit()