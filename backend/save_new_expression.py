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
conn.set_session(autocommit=True)
cursor = conn.cursor()


test_expression = {'lang': 'si', 
         'expr': 'dan', 
         'realizations': 'dan-0', 
         'glosses': 'day-NOM/ACC.SG', 
         'lemmas': 'dan', 
         'poses': 'N'
         }

def insert_expression(received_expression: dict[str:str]):
    expression_object = process_json.Expression.create_expr(
        expression=received_expression['expr'],
        realization=received_expression['realizations'],
        lemmas=received_expression['lemmas'],
        pos=received_expression['poses'],
        glossing=received_expression['glosses'])
    
    # cursor.execute("""SELECT MAX(expr_id) FROM public.expressions""")
    # last_id_before = cursor.fetchone()[0]
    # print('last id before', last_id_before)
    last_inserted = filling(received_expression['lang'], expression_object)
    
    # if last_id_before < last_inserted:
    #     return 'ok'
    # else:
    return last_inserted

# insert_expression(test_expression)