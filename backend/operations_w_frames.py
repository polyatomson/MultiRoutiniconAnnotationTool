import config
import psycopg2
from markupsafe import escape
from save_new_frame import insert_frame
import re
from create_db import filling
import process_json

conn = psycopg2.connect(database=config.DATABASE,
                        host=config.DB_HOST,
                        user=config.DB_USER,
                        password=config.DB_PASSWORD,
                        port=config.DB_PORT)
conn.set_session()
cursor = conn.cursor()


def get_events(stage: str) -> list[str]:
    cursor.execute("""SELECT "event" from public.events_popularity_by_stage where stage=%s;""", (stage,))
    events = cursor.fetchall()
    if events != []:
        return [e[0] for e in events]
    else:
        cursor.execute("""SELECT "event" from public.events ORDER BY "event";""")
        events = cursor.fetchall()
        return [e[0] for e in events]

def get_triggers() -> list[str]:
    cursor.execute("""SELECT "event" from public.events_popularity_by_stage where stage='trigger';""")
    events = cursor.fetchall()
    if events != []:
        return [e[0] for e in events]
    else:
        cursor.execute("""SELECT "event" from public.events ORDER BY "event";""")
        events = cursor.fetchall()
        return [e[0] for e in events]

def get_effects() -> list[str]:
    cursor.execute("""SELECT "event" from public.events_popularity_by_stage where stage='effect';""")
    events = cursor.fetchall()
    if events != []:
        return [e[0] for e in events]
    else:
        cursor.execute("""SELECT "event" from public.events ORDER BY "event";""")
        events = cursor.fetchall()
        return [e[0] for e in events]
    
def get_actions() -> list[str]:
    cursor.execute("""SELECT "event" from public.events_popularity_by_stage where stage='action';""")
    events = cursor.fetchall()
    if events != []:
        return [e[0] for e in events]
    else:
        cursor.execute("""SELECT "event" from public.events ORDER BY "event";""")
        events = cursor.fetchall()
        return [e[0] for e in events]

def get_pragmatics(struct: str) -> list[str]:
    cursor.execute("""SELECT pragmatics from pragmatics_pop_by_structure WHERE struct=%s;""", (struct, ))
    pragmatics = cursor.fetchall()
    return [p[0] for p in pragmatics]

def get_sit_tags() -> list[str]:
    cursor.execute("""SELECT situation_tag from st_popularity;""")
    st = cursor.fetchall()
    return [tag[0] for tag in st]

def get_tags_on_structure(struct: str) -> dict:
    pragmatics = get_pragmatics(struct)
    if struct == 'reaction':
        triggers = get_events('trigger')
        return {'p': pragmatics, 't': triggers}
    elif struct == 'reaction + prompt':
        triggers = get_events('trigger')
        effects = get_events('effect')
        return {'p': pragmatics, 't': triggers, 'e': effects}
    elif struct == 'prompt':
        effects = get_events('effect')
        return {'p': pragmatics, 'e': effects}
    elif struct == 'accompaniment':
        triggers = get_events('trigger')
        effects = get_events('effect')
        actions = get_events('action')
        return {'p': pragmatics, 't': triggers, 'a': actions, 'e': effects}
    else:
        raise ValueError('non-existant structure')

def get_routines():
    cursor.execute("""select json_agg(vr) from vacant_routines vr;""")
    routines = cursor.fetchall()
    try:
        return routines[0][0]
    except:
        return []

def get_conditions():
    cursor.execute("""select json_agg(c_pop) from conditions_pop c_pop where category != 'empty';""")
    conditions = cursor.fetchall()
    try:
        return conditions[0][0]
    except:
        return []

def get_general_frame_tags():
    structure_tags = get_tags_on_structure('accompaniment')
    situation_tags = get_sit_tags()
    routines = get_routines()
    conditions = get_conditions()
    return {'structure': structure_tags, 'stags': situation_tags, 'conditions': conditions, 'routines': routines}

def get_linked_routines(frame_id: int):
    cursor.execute("""select r2f.routine_id, "routine", "lang"
                   from routines2frames r2f 
                   left join "routines" r on r2f.routine_id = r.routine_id
                   left join langs l on r.lang_id = l.lang_id
                   where frame_id = %s""", (frame_id, ))
    routines = [{'routine_id': r[0], 'routine': r[1], 'lang': r[2]} for r in cursor.fetchall()]
    return {'routines': routines}

def delete_frame(frame_id: int):
    cursor.execute("""with deleted_f2p as (delete from frames2pragmatics where frame_id = %(frame_id)s),
                   deleted_f2e as (delete from frames2events where frame_id = %(frame_id)s),
                   deleted_f2st as (delete from frames2st where frame_id = %(frame_id)s),
                   deleted_f2c as (delete from frames2conditions where frame_id = %(frame_id)s),
                   r2frame_ids as (select routines2frames_id from routines2frames where frame_id = %(frame_id)s),
                   unlinked_examples as (update "examples" set routines2frames_id = null where routines2frames_id = any(select routines2frames_id from r2frame_ids)),
                   deleted_r2f as (delete from routines2frames where routines2frames_id = any(select routines2frames_id from r2frame_ids))
                   delete from frames where frame_id = %(frame_id)s;""",
                   {'frame_id': frame_id})
    conn.commit()
    return {'deleted': frame_id}

def save_edits(data) -> dict:
    frame_id = data['frame_id']
    keep_linked = data['keepLinked']
    unlink = [r_id for r_id in data['linkedRoutines'] if r_id not in keep_linked]
    data['examples'] = []
    frame_new = insert_frame(data)
    if frame_new['added'] is False and frame_new['frame_id'] == frame_id:
        return {'status': 'unchanged'}
    for routine_id in unlink:
        cursor.execute("""update routines2frames set frame_id = %s where routine_id = %s and frame_id=%s;""", (frame_new['frame_id'], routine_id, frame_id))
        conn.commit()
    if keep_linked == []:
        delete_frame(frame_id)
        return {'status': 'saved', 'new_frame': frame_new['frame_id']}
    return {'status': 'changed', 'new_frame': frame_new['frame_id'], 'old_frame': frame_id}

# test = {
#     "events": {
#         "triggers": [
#             "danger"
#         ],
#         "actions": [],
#         "effects": [
#             "help [a]"
#         ]
#     },
#     "tags": [
#         "accident"
#     ],
#     "pragmatics": [
#         "cry of distress",
#         "summoning",
#         "smth"
#     ],
#     "conditions": [
#         {
#             "category": "relationship",
#             "condition": "The speaker is not addressing any specific person. ",
#             "condition_id": "99"
#         }
#     ],
#     "sitStructure": "reaction + prompt",
#     "examples": [],
#     "frame_id": 31,
#     "keepLinked": [
#         37
#     ],
#     "linkedRoutines": [
#         1,
#         50,
#         37
#     ]
# }

# res = save_edits(test)
# res = get_routines()
# res = get_conditions()    
# print()

# res = get_events('action')
# print()

# res = get_pragmatics('reaction + prompt')
# print()

# res = get_sit_tags()
# print()

# get_effects()
# get_actions()
# get_triggers()
