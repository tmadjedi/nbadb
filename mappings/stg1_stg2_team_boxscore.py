import psycopg2

conn = psycopg2.connect("dbname='nba' user='nba' host='localhost'")
cur = conn.cursor()

cur.execute("""
    INSERT INTO stg2_team_boxscore
    SELECT b.game_id
          ,b.team_id
          ,s.season_id
          ,SUM(b.fgm)
          ,SUM(b.fga)
          ,SUM(b.fgm) / SUM(b.fga)::REAL
          ,SUM(b.fg3m)
          ,SUM(b.fg3a)
          ,SUM(b.fg3m) / SUM(b.fg3a)::REAL
          ,SUM(b.ftm)
          ,SUM(b.fta)
          ,SUM(b.ftm) / SUM(b.fta)::REAL
          ,SUM(b.oreb)
          ,SUM(b.dreb)
          ,SUM(b.reb)
          ,SUM(b.ast)
          ,SUM(b.stl)
          ,SUM(b.blk)
          ,SUM(b.tov)
          ,SUM(b.pf)
          ,SUM(b.pts)
          ,RANK() OVER (PARTITION BY s.season_id, b.team_id ORDER BY b.game_id)
          ,RANK() OVER (PARTITION BY b.game_id ORDER BY SUM(b.pts) DESC)
      FROM stg1_boxscore b
      JOIN stg2_season s
        ON SUBSTRING(b.game_id FROM 3 for 1) = to_char(s.season_type_code, 'FM9')
       AND SUBSTRING(b.game_id FROM 4 for 2) = to_char(s.season_year % 100, 'FM09')
     GROUP BY b.game_id, b.team_id, s.season_id
        ON CONFLICT DO NOTHING
""")

conn.commit()
cur.close()
conn.close()