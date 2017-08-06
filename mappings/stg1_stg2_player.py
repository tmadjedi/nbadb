import psycopg2
from psycopg2.extras import execute_values

conn = psycopg2.connect("dbname='nba' user='nba' host='localhost'")
cur = conn.cursor()

cur.execute("""
    SELECT DISTINCT b.player_id 
          ,b.player_name
      FROM stg1_boxscore b
    EXCEPT
    SELECT t.player_id
          ,t.player_name
      FROM stg2_player t
    """)
new = cur.fetchall()

# TODO: pick scd type to implement
execute_values(cur, """
    INSERT INTO stg2_player (player_id, player_name)
    VALUES %s""",
    new)

conn.commit()
cur.close()
conn.close()
