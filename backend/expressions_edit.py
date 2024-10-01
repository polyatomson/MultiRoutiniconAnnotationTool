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

def export_table(lang: str) -> list:
    cursor.execute("SELECT expr_full FROM expressions WHERE lang_id=%s", (lang,))
    expressions = cursor.fetchall()
    expressions = [e[0] for e in expressions]
    try:
        return {'expressions': expressions}
    except:
        return {'expressions': None}

# def update_expr(expr: dict):
#     gloss_id = escape(gloss_row['gloss_id'])
#     gloss = escape(gloss_row['gloss'])
#     lex = escape(gloss_row['lex'])
#     gl_class = escape(gloss_row['class'])
#     try:
#         cursor.execute("UPDATE glosses SET gloss=%s, lex=%s, class=%s WHERE gloss_id = %s",
#                     (gloss, lex, gl_class, gloss_id))
#         return "gloss sucessfully updated"
#     except Exception as ex:
#         return ex
    
def get_annotated_exprs(lang: str) -> dict:
    cursor.execute("""SELECT jsonb_agg(t) FROM (SELECT * FROM all_expressions WHERE lang=%s) t;""", (lang, ))
    res = cursor.fetchone()[0]
    if res is None:
        return []
    else:
        return res

def get_annotated_expr_by_id(expr_id: int) -> dict:
    cursor.execute("""SELECT jsonb_agg(t) FROM (SELECT * FROM all_expressions WHERE expr_id=%s) t;""", (expr_id, ))
    res = cursor.fetchone()[0]
    if res is None:
        return []
    else:
        return res
    
def rereference_exprs(routine_id: int, expr_ids: list[int]) -> dict[str, str]:
    cursor.execute("""SELECT expr_id FROM routines2expressions WHERE routine_id=%s;""", (routine_id,))
    expr_ids_db = [expr_id[0] for expr_id in cursor.fetchall()]
    to_remove = [expr_id for expr_id in expr_ids_db if expr_id not in expr_ids]
    to_add = [expr_id for expr_id in expr_ids if expr_id not in expr_ids_db]
    status = {}
    if to_add != []:
        cursor.executemany("""INSERT INTO routines2expressions (expr_id, routine_id) VALUES (%s, %s)""", 
                       [(expr_id, routine_id) for expr_id in to_add])
        status['n_added'] = cursor.rowcount
    if to_remove != []:
        cursor.executemany("""DELETE FROM routines2expressions WHERE expr_id = %s AND routine_id = %s""",
                       [(expr_id, routine_id) for expr_id in to_remove])
        status['n_deleted'] = cursor.rowcount
    conn.commit()
    return status

# rereference_exprs(50, [225])
# export_table(49)
# update_gloss(425, 'nom/acc', False, 'case')
# export_table()

# res = get_annotated_exprs('ru')