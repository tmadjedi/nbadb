import json, psycopg2, os
from psycopg2.extras import execute_values

# path to source json files
path = '../source_data/box/'

# password from .pgpass file
conn = psycopg2.connect("dbname='nba' user='nba' host='localhost'")
cur = conn.cursor()

for root, dirs, files in os.walk(path):
    for file in files:

        cur.execute("""
            SELECT *
              FROM stg1_loaded
             WHERE file_name = %s
            """,
            (file,))

        if not cur.fetchall():
            print("loading", file)
        else:
            print(file, "already loaded")
            continue

        f = open(path + file)
        data = json.load(f)
        values = [tuple(x) for x in data['resultSets'][0]['rowSet']]
        
        try:
            execute_values(cur, """
                INSERT INTO stg1_boxscore
                VALUES %s""",
                values)

            cur.execute("""
                INSERT INTO stg1_loaded
                VALUES (%s)""",
                (file,))
            conn.commit()
        except psycopg2.Error as e:
            print(e.pgerror, "at file", file)

cur.close()
conn.close()