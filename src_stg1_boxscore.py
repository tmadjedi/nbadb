import json, psycopg2
from psycopg2.extras import execute_values

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
            min INTERVAL,
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

file = open('../0041600212_box.json')
data = json.load(file)
values = [tuple(x) for x in data['resultSets'][0]['rowSet']]

# password from .pgpass file
conn = psycopg2.connect("dbname='nba' user='nba' host='localhost'")
cur = conn.cursor()

# create table
create_boxscore(cur)
conn.commit()

# insert values
execute_values(cur, """
    INSERT INTO boxscore
    VALUES %s""",
    values)
conn.commit()

cur.close()
conn.close()