import config
import psycopg2
from markupsafe import escape

from create_db import filling
import process_json

conn = psycopg2.connect(database=config.DATABASE,
                        host=config.DB_HOST,
                        user=config.DB_USER,
                        password=config.DB_PASSWORD,
                        port=config.DB_PORT)
conn.set_session(readonly=True)
cursor = conn.cursor()

def get_glossing_examples(gl_id: int):
    gl_id = str(gl_id)
    cursor.execute(open("sql_queries/get_units_glossed_this_way.sql", 'r').read(), (gl_id,))
    res = cursor.fetchall()[0][0]
    if res is None:
        return {'langs':{}, 'n': 0, 'examples': []}
    langs = {item['lang'] for item in res}
    lang_stats = {lang:len([item for item in res if item['lang'] == lang]) for lang in langs}
    for i, item in enumerate(res):
        morphs = [morph_gl['morph'] for morph_gl in item['glossing']]
        glosses = ['.'.join(morph_gl['glossed']) for morph_gl in item['glossing']]
        reorganized = {'morphs': morphs, 'glosses': glosses}
        res[i]['glossing'] = reorganized
    return {'lang_stats':lang_stats, 'n':len(res), 'examples': res}

# test = get_glossing_examples(0)
# test = get_glossing_examples(963)
# print(test)