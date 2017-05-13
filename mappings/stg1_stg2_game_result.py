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
          ,(SELECT s.season_id
              FROM stg2_season s
             WHERE to_char(s.season_type_code, 'FM9') = SUBSTRING(b.game_id FROM 3 FOR 1)
               AND to_char(s.season_year % 100, 'FM09') = SUBSTRING(b.game_id FROM 4 FOR 2)) AS season_id
          ,g1.team_id AS winner_team_id
          ,g1.pts AS winner_pts
          ,g2.team_id AS loser_team_id
          ,g2.pts AS loser_pts
      FROM 
           (SELECT DISTINCT game_id
              FROM stg1_boxscore) b
      JOIN game_team_rank g1 
        ON b.game_id = g1.game_id and g1.rank = 1
      JOIN game_team_rank g2
        ON b.game_id = g2.game_id and g2.rank = 2
     ORDER BY b.game_id
        ON CONFLICT DO NOTHING
""")

conn.commit()
cur.close()
conn.close()