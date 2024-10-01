import config
import psycopg2
from markupsafe import escape
from typing import Optional

conn = psycopg2.connect(database=config.DATABASE,
                        host=config.DB_HOST,
                        user=config.DB_USER,
                        password=config.DB_PASSWORD,
                        port=config.DB_PORT)
cursor = conn.cursor()

def routines_from_db(lang_id: Optional[list[int]] = None) -> dict:
    print('frames_from_db_input', lang_id)
    if lang_id == []:
        cursor.execute("""select jsonb_agg(t) from (select * from routines_full_w_cxs) t;
                            """)
    else:
        cursor.execute("""select jsonb_agg(t) from (select * from routines_full_w_cxs where lang_id=ANY(%s)) t;""", (lang_id, ))
    table = cursor.fetchone()[0]
    return table

def routines_bare(lang_id: Optional[int]):
    if lang_id:
        cursor.execute("""select r."routine" from "routines" r where r.lang_id = %s""", (lang_id, ))
        table = cursor.fetchall()
        if table is None:
            return table
        else:
            table = [r[0] for r in table]
            return table
    else:
        cursor.execute("""select jsonb_agg(t) from (select r."routine", r.routine_id, l.lang from "routines" r left join langs l on r.lang_id = l.lang_id order by r.lang_id, r."routine") t;""")
        table = cursor.fetchone()[0]
        return table

def get_routine(routine_id: int) -> list[dict]:
    try:
        assert type(routine_id) == int
    except:
        return {"error": "The id has to be integer"}
    cursor.execute("""select jsonb_agg (t) from (select * from routines_aggregated where routine_id = %s) t""", (routine_id, ))
    routine_info = cursor.fetchone()
    # print(routine_info)
    if routine_info[0] is None:
        return {"error": "No routines with this id"}
    else:
        return routine_info[0][0]

get_routine(0)
# routines_from_db()
    
        