import psycopg2
from psycopg2.extras import execute_values

conn = psycopg2.connect("dbname='nba' user='nba' host='localhost'")
cur = conn.cursor()

# find the rows that have changed
cur.execute("""
    SELECT g.game_key 
          ,t.team_key
          ,s.season_key
          ,SUM(b.fgm)
          ,SUM(b.fga)
          ,SUM(b.fgm)::REAL / SUM(b.fga)::REAL
          ,SUM(b.fg3m)
          ,SUM(b.fg3a)
          ,SUM(b.fg3m)::REAL / SUM(b.fg3a)::REAL
          ,SUM(b.ftm)
          ,SUM(b.fta)
          ,SUM(b.ftm)::REAL / SUM(b.fta)::REAL
          ,SUM(b.oreb)
          ,SUM(b.dreb)
          ,SUM(b.reb)
          ,SUM(b.ast)
          ,SUM(b.stl)
          ,SUM(b.blk)
          ,SUM(b.tov)
          ,SUM(b.pf)
          ,SUM(b.pts)
          ,RANK() OVER (PARTITION BY s.season_key, t.team_key ORDER BY b.game_id)
          ,(RANK() OVER (PARTITION BY b.game_id ORDER BY SUM(b.pts))) - 1
      FROM stg1_boxscore b
      JOIN stg2_season s
        ON SUBSTRING(b.game_id FROM 3 for 1) = to_char(s.season_type_code, 'FM9')
       AND SUBSTRING(b.game_id FROM 4 for 2) = to_char(s.season_year % 100, 'FM09')
      JOIN stg2_team t
        ON t.team_id = b.team_id
      JOIN stg2_game g
        ON g.game_id = b.game_id
     GROUP BY g.game_key, b.game_id, t.team_key, s.season_key
    EXCEPT
    SELECT *
      FROM stg2_team_boxscore
""")
new = cur.fetchall()

execute_values(cur, """
    INSERT INTO stg2_team_boxscore
    VALUES %s
        ON CONFLICT (game_key, team_key) DO
    UPDATE SET (fgm, fga, fg_pct, fg3m, fg3a, fg3_pct, ftm, fta, ft_pct, oreb, dreb, reb, ast, stl, blk, tov, pf, pts, game_of_season, game_rank) = 
    (EXCLUDED.fgm, EXCLUDED.fga, EXCLUDED.fg_pct, EXCLUDED.fg3m, EXCLUDED.fg3a, EXCLUDED.fg3_pct, EXCLUDED.ftm, EXCLUDED.fta, EXCLUDED.ft_pct, EXCLUDED.oreb, EXCLUDED.dreb, EXCLUDED.reb, EXCLUDED.ast, EXCLUDED.stl, EXCLUDED.blk, EXCLUDED.tov, EXCLUDED.pf, EXCLUDED.pts, EXCLUDED.game_of_season, EXCLUDED.game_rank)""",
    new)

conn.commit()
cur.close()
conn.close()
