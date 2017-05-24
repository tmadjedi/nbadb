import psycopg2

conn = psycopg2.connect("dbname='nba' user='nba' host='localhost'")
cur = conn.cursor()



conn.commit()
cur.close()
conn.close()