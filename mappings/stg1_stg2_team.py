import psycopg2
from psycopg2.extras import execute_values

conn = psycopg2.connect("dbname='nba' user='nba' host='localhost'")
cur = conn.cursor()

cur.execute("""
    SELECT DISTINCT b.team_id
          ,b.team_abbreviation
      FROM stg1_boxscore b
    EXCEPT
    SELECT t.team_id
          ,t.team_abbreviation
      FROM stg2_team t
    """)
new = cur.fetchall()

# TODO: pick scd type to implement
execute_values(cur, """
    INSERT INTO stg2_team (team_id, team_abbreviation)
    VALUES %s""",
    new)

conn.commit()
cur.close()
conn.close()