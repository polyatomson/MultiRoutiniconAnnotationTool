import config
import psycopg2
from markupsafe import escape

conn = psycopg2.connect(database=config.DATABASE,
                        host=config.DB_HOST,
                        user=config.DB_USER,
                        password=config.DB_PASSWORD,
                        port=config.DB_PORT)
conn.set_session(autocommit=True)
cursor = conn.cursor()

def export_table():
    cursor.execute("""SELECT json_agg(t) FROM (
                   SELECT gloss_id,
                    CASE WHEN lex = false THEN UPPER(gloss)
                         ELSE LOWER(gloss)
                    END AS gloss_value
                   FROM glosses
                   WHERE useless = false
                   ORDER BY gloss) t""")
    glosses = cursor.fetchall()[0]
    return glosses[0]


# res = export_table()
# print(res)