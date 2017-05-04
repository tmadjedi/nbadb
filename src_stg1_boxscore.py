import json, psycopg2, os
from psycopg2.extras import execute_values

def load_boxscore(cur, values):
    execute_values(cur, """
        INSERT INTO boxscore
        VALUES %s""",
        values)

def log_load(cur, file):
    cur.execute("""
        INSERT INTO loaded
        VALUES (%s)""",
        file)

# password from .pgpass file
conn = psycopg2.connect("dbname='nba' user='nba' host='localhost'")
cur = conn.cursor()
path = '../source_data/box/'

for root, dirs, files in os.walk(path):
    for file in files:
        print("loading", file)

        f = open(path + file)
        data = json.load(f)
        values = [tuple(x) for x in data['resultSets'][0]['rowSet']]
        
        try:
            load_boxscore(cur, values)
            log_load(cur, file)
            conn.commit()
        except:
            print("failed loading", file)

cur.close()
conn.close()