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

def language_poses(lang_id: int) -> list:
    cursor.execute("""select distinct(pos) 
                   from public.units
                   where lang_id=%s""", (lang_id,))
    poses = cursor.fetchall()
    try:
        return [l[0] for l in poses]
    except:
        return []


# res = language_poses(49)
# print(res)