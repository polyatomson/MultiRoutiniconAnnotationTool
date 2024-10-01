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

def export_table():
    cursor.execute("""SELECT json_agg(t) FROM (SELECT *, 
                   ROW_NUMBER() OVER (ORDER BY gloss) 
                   FROM glosses
                   WHERE useless = false) t""")
    glosses = cursor.fetchall()[0]
    return glosses[0]

def update_gloss(gloss_row: dict):
    gloss_id = escape(gloss_row['gloss_id'])
    gloss = escape(gloss_row['gloss'])
    lex = escape(gloss_row['lex'])
    gl_class = escape(gloss_row['class'])
    if gloss_id != 'new':
        print('here')
        try:
            cursor.execute("UPDATE glosses SET gloss=%s, lex=%s, class=%s WHERE gloss_id = %s",
                        (gloss, lex, gl_class, gloss_id))
            return {'action':'updated'}
        except Exception as ex:
            return ex
    elif gloss.strip() != '':
        try:
            cursor.execute("INSERT INTO glosses (gloss, lex, class) VALUES (%s, %s, %s) RETURNING gloss_id",
                        (gloss, lex, gl_class,))
            new_gloss_id = cursor.fetchone()[0]
            print('newly added id', new_gloss_id)
            return {'action':'inserted', 'new_gloss_id':new_gloss_id}
        except Exception as ex:
            # print(ex)
            return ex

def remove_gloss(gloss_id):
    try:
        cursor.execute("UPDATE glosses SET useless=true WHERE gloss_id = %s",
        (gloss_id,))
        return f'gloss with id{gloss_id} is marked useless'
    except Exception as ex:
        return ex

# # res = export_table()
# # res1 = update_gloss({'gloss_id':425, 'gloss':'nom/acc', 'lex':False, 'class':'case'})
# res = update_gloss({'gloss_id':'new', 'gloss':'loc', 'lex':False, 'class':'conversive'})
# # print(res1)
# print(res)
# export_table()
# res = remove_gloss(521)
# res = export_table()
# print(res)