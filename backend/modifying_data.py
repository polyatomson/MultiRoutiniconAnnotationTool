import config
import psycopg2

conn = psycopg2.connect(database=config.DATABASE,
                        host=config.DB_HOST,
                        user=config.DB_USER,
                        password=config.DB_PASSWORD,
                        port=config.DB_PORT)
cursor = conn.cursor()

def delete_routine(routine_id: int):
    cursor.execute(
    """with deleted_f2r as (delete from routines2frames rf where rf.routine_id = %(r_id)s returning rf.routines2frames_id),
    unlinked_examples as (update examples e set routines2frames_id = null where e.routines2frames_id = df.routines2frames_id from (select * from deleted_f2r) df),
    deleted_r2e as (delete from routines2expressions re where re.routine_id = %(r_id)s),
    deleted_reds as (delete from cx_reductions cr where cr.routine_id = %(r_id)s),
    deleted_cx_examples as (delete from examples4cxs ec where ec.routine_id = %(r_id)s),
    deleted_r2cx as (delete from routines2cxs rc where rc.routine_id = %(r_id)s)
    delete from "routines" r where r.routine_id = %(r_id)s;""",
    {'r_id': routine_id}
    )
    conn.commit()
    return {'message': 'deleted'}

def change_frame_info(frame: dict):
    try:
        cursor.execute("""update routines2frames set comments = %(comments)s, definition = %(definition)s,
                   intonation = %(intonation)s where routine_id = %(routine_id)s and frame_id = %(frame_id)s returning routines2frames_id;""",
                   frame)
    except Exception as ex:
        return {'error': str(ex)}
    r2f_id = cursor.fetchone()[0]
    examples: list[dict] = frame['examples'] or []
    to_update = [e for e in examples if 'example_id' in e]
    to_keep_ids = [e['example_id'] for e in to_update]
    new_examples = [e | {'routines2frames_id': r2f_id} for e in examples if 'example_id' not in e]
    cursor.execute("""select example_id from examples where routines2frames_id = %s""", (r2f_id, ))
    examples_in_db = [e[0] for e in cursor.fetchall()]
    to_unlink_ids = [e_id for e_id in examples_in_db if e_id not in to_keep_ids]
    try:
        if to_unlink_ids != []:
            cursor.execute("""update "examples" set routines2frames_id = null where example_id = any(%s)""", (to_unlink_ids, ))
        if new_examples != []:
            cursor.executemany("""insert into examples (routines2frames_id, "example", ex_source, dated, "translation")
                    values(%(routines2frames_id)s, %(example)s, %(source)s, %(dated)s, %(translation)s);""", new_examples)
        if to_update != []:
            cursor.executemany("""update examples set "example"=%(example)s, ex_source=%(source)s,
                        dated=%(dated)s, "translation"=%(translation)s where example_id = %(example_id)s""", to_update)
    except Exception as ex:
        return {'error': str(ex)}

    conn.commit()
    return {'status': 'ok'}

test = {
  "comments": None,
  "definition": "snt2",
  "examples": [],
  "frame_id": 44,
  "intonation": None,
  "pragmatics": [
    "cry of distress",
    "summoning"
  ],
  "sit_tags": [
    "accident",
    "danger"
  ],
  "situation_structure": "reaction",
  "situations": {
    "trigger": [
      "danger"
    ]
  },
  "usage_conditions": [
    {
      "category": "relationship",
      "condition": "The speaker is not addressing any specific person. ",
      "condition_id": "99"
    }
  ],
  "routine_id": 48
}

# change_frame_info(test)