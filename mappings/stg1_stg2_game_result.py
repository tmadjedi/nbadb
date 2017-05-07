import psycopg2

conn = psycopg2.connect("dbname='nba' user='nba' host='localhost'")
cur = conn.cursor()

cur.execute("""
    WITH game_team_rank AS (
         SELECT game_id
               ,team_id
               ,SUM(pts) AS pts
               ,rank() over (partition by game_id ORDER BY SUM(pts) DESC) AS rank
          FROM stg1_boxscore
         GROUP BY game_id, team_id
         ORDER BY game_id)
    INSERT INTO stg2_game_result
    SELECT b.game_id
          ,g1.team_id as winner_team_id
          ,g1.pts as winner_pts
          ,g2.team_id as loser_team_id
          ,g2.pts as loser_pts
     FROM 
          (SELECT DISTINCT game_id
             FROM stg1_boxscore) b
     JOIN game_team_rank g1 
       ON b.game_id = g1.game_id and g1.rank = 1
     JOIN game_team_rank g2
       ON b.game_id = g2.game_id and g2.rank = 2
    ORDER BY game_id
""")

conn.commit()
cur.close()
conn.close()