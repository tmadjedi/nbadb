import psycopg2

conn = psycopg2.connect("dbname='nba' user='nba' host='localhost'")
cur = conn.cursor()

cur.execute("""
    INSERT INTO stg2_season
    SELECT DISTINCT SUBSTRING(game_id from 1 for 3)
          ,SUBSTRING(game_id from 4 for 2)
      FROM stg2_game_result
        ON CONFLICT DO NOTHING
    """)

conn.commit()
cur.close()
conn.close()