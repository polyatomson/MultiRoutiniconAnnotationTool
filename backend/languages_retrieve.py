import config
import psycopg2
from markupsafe import escape

conn = psycopg2.connect(database=config.DATABASE,
                        host=config.DB_HOST,
                        user=config.DB_USER,
                        password=config.DB_PASSWORD,
                        port=config.DB_PORT)
conn.set_session(readonly=True)
cursor = conn.cursor()

def export_table():
    cursor.execute("""SELECT JSON_AGG(t) from
                   (select langs.lang, langs.lang_id
                   from public.langs) t""")
    try:
        languages = cursor.fetchall()[0][0]
        # languages_dict = {k:v for language in languages for k,v in language.items() }
        return languages
    except:
        return []

# export_table()
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
    

# export_table()
# update_gloss(425, 'nom/acc', False, 'case')
# export_table()