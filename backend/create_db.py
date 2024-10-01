import config
import psycopg2
# import re
import process_json
import json
from mini_handlers import sort_glosses



conn = psycopg2.connect(database=config.DATABASE,
                        host=config.DB_HOST,
                        user=config.DB_USER,
                        password=config.DB_PASSWORD,
                        port=config.DB_PORT)
conn.set_session(autocommit=True)
global cursor
cursor = conn.cursor()

def inserting_lang(lang: str, insert_sql_fn: str="sql_queries/insert_lang.sql", id_sql_fn: str="sql_queries/id_lang.sql") -> int:
    try:
        cursor.execute(open(id_sql_fn, "r").read(), (lang,))
        return cursor.fetchone()[0]
    except:
        cursor.execute(open(insert_sql_fn, "r").read(), (lang,))
        return cursor.fetchone()[0]

def inserting_expr(expr: str, glossing: str, lang_id: int, insert_sql_fn: str="sql_queries/insert_expression.sql", id_sql_fn: str="sql_queries/id_expression.sql") -> int:
    try:
        cursor.execute(open(insert_sql_fn, "r").read(), (expr, glossing, lang_id,))
        return cursor.fetchone()[0]
    except:
        # print("the expression already exists, returning its id")
        cursor.execute(open(id_sql_fn, "r").read(), (expr, glossing, lang_id,))
        return cursor.fetchone()[0]

def inserting_unit(unit: str, lang_id: int, lemma: int, pos: str, realization: str, glossing: str, insert_sql_fn: str="sql_queries/insert_unit.sql", id_sql_fn: str="sql_queries/id_unit.sql") -> int:
    try:
        cursor.execute(open(insert_sql_fn, "r").read(), (unit,lang_id,lemma,pos,realization, glossing,))
        return cursor.fetchone()[0]
    except Exception as ex:
        cursor.execute(open(id_sql_fn, "r").read(), (unit,lang_id,lemma,pos,realization, glossing,))
        return cursor.fetchone()[0]

def connect_expr2units(unit_id: int, expr_id: int, place: int, insert_sql_fn: str="sql_queries/insert_ex2un.sql"):
    cursor.execute(open(insert_sql_fn, "r").read(), (expr_id,unit_id,place,))


def inserting_morphs(morph, lang_id, gloss: str, insert_sql_fn: str="sql_queries/insert_morph.sql", id_sql_fn: str="sql_queries/id_morph.sql") -> int:
    try:
        cursor.execute(open(insert_sql_fn, "r").read(), (morph,lang_id,gloss))
        return cursor.fetchone()[0]
    except Exception as ex:
        cursor.execute(open(id_sql_fn, "r").read(), (morph,lang_id,gloss))
        return cursor.fetchone()[0]

def inserting_gloss(gloss: process_json.Gloss, insert_sql_fn: str="sql_queries/insert_gloss.sql", id_sql_fn: str="sql_queries/id_gloss.sql") -> int:
    try:
        cursor.execute(open(insert_sql_fn, "r").read(), (gloss.gloss.lower(), gloss.lex, gloss.gl_class,))
        return cursor.fetchone()[0]
    except Exception as ex:
        cursor.execute(open(id_sql_fn, "r").read(), (gloss.gloss.lower(), gloss.lex,))
        return cursor.fetchone()[0]

def connect_morph2gloss(morph_id: int, gl_id: int, insert_sql_fn: str="sql_queries/insert_m2gl.sql"):
    cursor.execute(open(insert_sql_fn, "r").read(), (morph_id,gl_id,))

def connect_morph2unit(morph_id: int, unit_id: int, place:int, insert_sql_fn: str="sql_queries/insert_m2unit.sql"):
    cursor.execute(open(insert_sql_fn, "r").read(), (morph_id,unit_id,place))

def filling(lang: str, expression: process_json.Expression):
    lang_id = inserting_lang(lang)
    # print("lang_id for", lang, lang_id)
    expr_id = inserting_expr(expression.expression, expression.full_glossing(), lang_id)
    # print("expr_id", expression.expression, lang_id, "=", expr_id)
    tokens = expression.units
    tokens_ids = [inserting_unit(t.unit, lang_id, t.lemma, t.pos, t.realization, t.glossing) for t in tokens]
    for place, t_id in enumerate(tokens_ids):
        connect_expr2units(t_id, expr_id, place+1)

    for i, token in enumerate(tokens):
        morphs = token.glossed_morphs
        for mplace, m in enumerate(morphs):
             morph_id = inserting_morphs(m.morph, lang_id, '.'.join(sort_glosses([gl.gloss for gl in m.glosses])))
             connect_morph2unit(morph_id, tokens_ids[i], mplace+1)
             for gl in m.glosses:
                gl_id = inserting_gloss(gl)
                connect_morph2gloss(morph_id, gl_id)
    return expr_id

def fill_from_json_file():
    dat = process_json.LangCollection.import_collection_from_file(config.DATA_SOURCE)
    lang = dat.lang
    for e in dat.collection:
        filling(lang, e)


def import_glosses_starter_pack(fn: str='glosses_starter_package_last.json'):
    with open(fn, 'r', encoding='utf-8') as fp:
        glosses = json.load(fp)['glosses']
    for gl in glosses:
        gl_class = gl['class'] if gl['class'] != '' else None
        ready_gloss = process_json.Gloss(gl['gloss'], gl['lex'], gl_class)
        inserting_gloss(ready_gloss)
    print('all starter pack glosses in db')

def default_fill():
    cursor.execute(open("sql_queries/create_schema.sql", "r").read())
    cursor.execute("SELECT * FROM expressions")
    in_db = cursor.fetchall()
    if in_db == []:
        import_glosses_starter_pack()
        print('filling the db from json')
        fill_from_json_file()
    cursor.execute("SELECT COUNT(*) FROM expressions")
    print("database contains:", cursor.fetchone()[0], "expressions")



if __name__ == '__main__':
    default_fill()



