import psycopg2

conn = psycopg2.connect("dbname='nba' user='nba' host='localhost'")
cur = conn.cursor()

cur.execute("""
    INSERT INTO stg2_season_result
    SELECT t.team_id
          ,s.season_type
          ,s.season_year,
          (SELECT COUNT(gr.winner_team_id)
             FROM stg2_game_result gr
            WHERE gr.winner_team_id = t.team_id
              AND SUBSTRING(gr.game_id FROM 1 for 3) = s.season_type
              AND SUBSTRING(gr.game_id FROM 4 for 2) = s.season_year) win_count,
          (SELECT count(gr.loser_team_id)
             FROM stg2_game_result gr
            WHERE gr.loser_team_id = t.team_id
              AND SUBSTRING(gr.game_id FROM 1 for 3) = s.season_type
              AND SUBSTRING(gr.game_id FROM 4 for 2) = s.season_year) loss_count
      FROM (SELECT DISTINCT team_id FROM stg1_boxscore) t
     CROSS JOIN stg2_season s
     ORDER BY s.season_year
             ,s.season_type
             ,win_count DESC
        ON CONFLICT DO NOTHING
""")

conn.commit()
cur.close()
conn.close()