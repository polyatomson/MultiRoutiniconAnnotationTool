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

def export_unit_info(lang_id: int, unit: str) -> list:
    cursor.execute("""select json_agg(t) 
                   from (select unit, realization, lemma, pos 
                   from public.units
                   where lang_id=%s and unit=%s) t""", (lang_id, unit,))
    analyses = cursor.fetchall()
    try:
        return analyses[0][0]
    except:
        return None
    
def export_mult_units_info(lang_id: int, units: list[str]) -> dict:
    mult_analyses = {}
    for unit in set(units):
        mult_analyses[unit] = export_unit_info(lang_id, unit)
    # print(mult_analyses)
    return mult_analyses
    
def change_routine(routine_id: int, new_routine_name: str) -> dict:
    try:
        cursor.execute("""UPDATE "routines" 
                   SET "routine" = %s WHERE routine_id = %s""",
                   (new_routine_name, routine_id, ))
        return {'status': 'ok'}
    except Exception as ex:
       return {'error': str(ex)} 

# res = export_mult_units_info(49, ['dan', 'noč', 'jutro'])
# print(res)

# # {'noč': None, 
# #  'jutro': [
# #      {'unit': 'jutro', 'realization': 'jutr-o', 'lemma': 'jutro', 'pos': 'N'}
# #      ], 
# #  'dan': [
# #      {'unit': 'dan', 'realization': 'dan-0', 'lemma': 'dan', 'pos': 'N'}, 
# #      {'unit': 'dan', 'realization': 'da-n', 'lemma': 'dati', 'pos': 'V'}
# #      ]
# #  }