import psycopg2
from psycopg2.extras import execute_values

conn = psycopg2.connect("dbname='nba' user='nba' host='localhost'")
cur = conn.cursor()

cur.execute("""
    SELECT b.team_key 
          ,b.season_key
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
     FROM stg2_team_boxscore b
    GROUP BY b.team_key
             ,b.season_key
   EXCEPT 
   SELECT *
     FROM stg2_team_season_boxscore
""")

new = cur.fetchall()

execute_values(cur, """
    INSERT INTO stg2_team_season_boxscore
    VALUES %s
        ON CONFLICT (team_key, season_key) DO
    UPDATE SET (fgm, fga, fg_pct, fg3m, fg3a, fg3_pct, ftm, fta, ft_pct, oreb, dreb, reb, ast, stl, blk, tov, pf, pts) = 
    (EXCLUDED.fgm, EXCLUDED.fga, EXCLUDED.fg_pct, EXCLUDED.fg3m, EXCLUDED.fg3a, EXCLUDED.fg3_pct, EXCLUDED.ftm, EXCLUDED.fta, EXCLUDED.ft_pct, EXCLUDED.oreb, EXCLUDED.dreb, EXCLUDED.reb, EXCLUDED.ast, EXCLUDED.stl, EXCLUDED.blk, EXCLUDED.tov, EXCLUDED.pf, EXCLUDED.pts)""",
    new)

conn.commit()
cur.close()
conn.close()