import config
import psycopg2
from markupsafe import escape
import json
from create_db import filling
import process_json
import re

conn = psycopg2.connect(database=config.DATABASE,
                        host=config.DB_HOST,
                        user=config.DB_USER,
                        password=config.DB_PASSWORD,
                        port=config.DB_PORT)
conn.set_session(autocommit=True)
cursor = conn.cursor()

def insert_frame(received_frame: dict[str:str]):
    # print(received_frame)
    struct = received_frame['sitStructure']
    pragm = json.dumps(received_frame['pragmatics'])
    if len(received_frame['conditions']) > 0:
        cond = json.dumps(received_frame['conditions'])
    else:
        cond = json.dumps([{'category': 'empty', 'condition': 'empty condition'}])
    tags = json.dumps(received_frame['tags'])
    events = received_frame['events']
    events = [{'stage':k.strip('s'), 'event_type': v} for k, values in events.items() for v in values]
    events = json.dumps(events)
    try:
        with open('sql_queries/inserting_frame.sql') as query:
                cursor.execute(query.read(), (struct, pragm, cond, tags, events))
    except Exception as ex:
         if ex.pgcode == '23505':
            uniquecode = re.findall(r"\(unique_code\)=\((.*?)\)", str(ex))[0]
            # print(uniquecode)
            cursor.execute("""SELECT frame_id FROM frames WHERE unique_code=%s""", (uniquecode,))
            existing_id = cursor.fetchone()[0]
            return {'added': False, 'frame_id': existing_id}
         else:
              raise ex
    frame_id: int = cursor.fetchone()[0]
    r_ids = [ex['r_id'] for ex in received_frame['examples']]
    r_ids = json.dumps(r_ids)
    with open('sql_queries/inserting_frame_examples.sql') as query:
        cursor.execute(query.read(), (r_ids, frame_id))
    return {'added': True, "frame_id": frame_id}

# test = {
#     'events': {
#         'triggers': ['greeting [a]']
#         }, 
#     'tags': [
#         'meeting'
#         ], 
#     'pragmatics': [
#         'greeting'
#         ], 
#     'conditions': [
#         ], 
#     'sitStructure': 'reaction', 
#     'examples': [
#         {'lang': 'ru', 'r': 'помогите', 'r_id': 1, 'vacant': True}
#         ], 
#     'frame_id': 'new1'}

# insert_frame(test)