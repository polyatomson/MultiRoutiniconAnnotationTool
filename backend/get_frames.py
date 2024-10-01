import config
import psycopg2
from markupsafe import escape
from typing import Optional

conn = psycopg2.connect(database=config.DATABASE,
                        host=config.DB_HOST,
                        user=config.DB_USER,
                        password=config.DB_PASSWORD,
                        port=config.DB_PORT)
conn.set_session()
cursor = conn.cursor()

def frames_from_db(lang_id: Optional[int] = None) -> dict:
    print('frames_from_db_input', lang_id)
    if lang_id is None:
        cursor.execute("""select jsonb_agg(t) from (
                            select af.frame_id, situation_structure, pragmatics, usage_conditions, sit_tags, situations, frame_examples,
                            case when count(r.routine_id) > 0 then jsonb_agg(
                       
                       jsonb_build_object('r_id', r.routine_id, 'r', r."routine", 'lang_id', r.lang_id, 'lang', l.lang)) else '[]'::jsonb end examples
                       
                            from 
                            all_frames_new af 
                            left join routines2frames rf on (af.frame_id =rf.frame_id)
                            left join "routines" r on (rf.routine_id=r.routine_id)
                            left join langs l on (r.lang_id = l.lang_id)
                            group by af.frame_id, situation_structure, pragmatics, usage_conditions, sit_tags, situations, frame_examples
                            ) t;
                            """)
    else:
        cursor.execute("""select jsonb_agg(t) from (
                       select af.frame_id, situation_structure, pragmatics, usage_conditions, sit_tags, situations, frame_examples,
                            case when count(r.routine_id) > 0 then jsonb_agg(
                       
                       jsonb_build_object('r_id', r.routine_id, 'r', r."routine", 'lang_id', r.lang_id, 'lang', l.lang)) else '[]'::jsonb end examples
                       
                            from 
                            all_frames_new af 
                            right join routines2frames rf on (af.frame_id =rf.frame_id)
                            left join "routines" r on (rf.routine_id=r.routine_id)
                            left join langs l on (r.lang_id = l.lang_id)
                       where r.lang_id = %s
                            group by af.frame_id, situation_structure, pragmatics, usage_conditions, sit_tags, situations, frame_examples
                            ) t;""", (lang_id, ))
    table = cursor.fetchone()[0]
    # if table is None:
    #     return
    # for i, row in enumerate(table):
    #     if len(row['examples']) > 3:
    #         table[i]['examples'] = row['examples'][0:3]
    # print(table)
    return table

def rereference_frames(routine_id: int, frame_ids: list[int]) -> dict[str, str]:
    cursor.execute("""SELECT frame_id FROM routines2frames WHERE routine_id=%s;""", (routine_id,))
    f_ids_in_db = [f_id[0] for f_id in cursor.fetchall()]
    to_remove = [f_id for f_id in f_ids_in_db if f_id not in frame_ids]
    to_add = [f_id for f_id in frame_ids if f_id not in f_ids_in_db]
    status = {}
    try:
        if to_add != []:
            cursor.executemany("""INSERT INTO routines2frames (frame_id, routine_id) VALUES (%s, %s)""", 
                        [(f_id, routine_id) for f_id in to_add])
            status['n_added'] = cursor.rowcount
        if to_remove != []:
            cursor.executemany("""
                            with unlink_ex as (UPDATE examples e SET routines2frames_id = null from (select routines2frames_id from routines2frames where routine_id = %(routine_id)s and frame_id = %(frame_id)s) r2f where r2f.routines2frames_id = e.routines2frames_id)
                            DELETE FROM routines2frames WHERE frame_id = %(frame_id)s AND routine_id = %(routine_id)s""",
                        [{'frame_id': frame_id, 'routine_id': routine_id} for frame_id in to_remove])
            status['n_deleted'] = cursor.rowcount
        conn.commit()
        if status == {}:
            status['n_changes'] = 0
        return status
    except Exception as ex:
        return {'error': str(ex)}


# frames_from_db()
    
        