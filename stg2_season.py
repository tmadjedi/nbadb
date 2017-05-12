import psycopg2
from psycopg2.extras import execute_values

conn = psycopg2.connect("dbname='nba' user='nba' host='localhost'")
cur = conn.cursor()

season_year = range(1980, 2030)
season_type_code = [1, 2, 3, 4]
season_type_descr = {
	1 : "Preseason",
	2 : "Regular Season",
	3 : "All Star",
	4 : "Post Season"
}

seasons = [(x, season_type_descr[x], y) for x in season_type_code for y in season_year]

execute_values(cur, """
	INSERT INTO stg2_season (season_type_code, season_type_descr, season_year)
	VALUES %s""",
	seasons)

conn.commit()
cur.close()
conn.close()