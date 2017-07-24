import psycopg2
from psycopg2.extras import execute_values

conn = psycopg2.connect("dbname='nba' user='nba' host='localhost'")
cur = conn.cursor()

cur.execute("""
    SELECT DISTINCT b.game_id
      FROM stg1_boxscore b
    EXCEPT
    SELECT g.game_id
      FROM stg2_game g
    """)
new = cur.fetchall()

execute_values(cur, """
    INSERT INTO stg2_game (game_id)
    VALUES %s""",
    new)

conn.commit()
cur.close()
conn.close()
