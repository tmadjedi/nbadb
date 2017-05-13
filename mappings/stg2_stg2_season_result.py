import psycopg2

conn = psycopg2.connect("dbname='nba' user='nba' host='localhost'")
cur = conn.cursor()

# TODO: Maybe a more elegant way to do this than a cross join to season?

cur.execute("""
    INSERT INTO stg2_season_result
    SELECT t.team_id
          ,to_char(s.season_type_code, '9')
          ,to_char(s.season_year % 100, '09')
          ,(SELECT count(distinct gr.game_id)
             FROM stg2_game_result gr
            WHERE gr.winner_team_id = t.team_id
              AND SUBSTRING(gr.game_id FROM 3 for 1) = to_char(s.season_type_code, 'FM9')
              AND SUBSTRING(gr.game_id FROM 4 for 2) = to_char(s.season_year % 100, 'FM09')) win_count,
          (SELECT count(gr.loser_team_id)
             FROM stg2_game_result gr
            WHERE gr.loser_team_id = t.team_id
              AND SUBSTRING(gr.game_id FROM 3 for 1) = to_char(s.season_type_code, 'FM9')
              AND SUBSTRING(gr.game_id FROM 4 for 2) = to_char(s.season_year % 100, 'FM09')) loss_count
      FROM (SELECT DISTINCT team_id FROM stg1_boxscore) t
     CROSS JOIN stg2_season s
     ORDER BY s.season_year
             ,s.season_type_code
             ,win_count DESC
        ON CONFLICT DO NOTHING
""")

conn.commit()
cur.close()
conn.close()