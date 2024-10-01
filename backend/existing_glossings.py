import config
import psycopg2
from markupsafe import escape
import re

conn = psycopg2.connect(database=config.DATABASE,
                        host=config.DB_HOST,
                        user=config.DB_USER,
                        password=config.DB_PASSWORD,
                        port=config.DB_PORT)
conn.set_session(autocommit=True)
cursor = conn.cursor()


def export_glossing(lang_id: int, unit: str, realization: str) -> list:
    cursor.execute(open("sql_queries/get_glossings.sql", "r").read(), (lang_id, realization,))
    glossed_morphs = cursor.fetchall()
    glossed_morphs = glossed_morphs[0][0]
    
    if glossed_morphs is None:
        morphs = re.split('-|=', realization)
        new_glossed_morphs = []
        for i, m in enumerate(morphs):
            new_glossed_morphs.append({
                'n': i+1,
                'unit': unit, 
                'morph': m,
                'picked_glosses': []})
            other_glosses = []
            cursor.execute(open("sql_queries/get_morph_glossing.sql", "r").read(), (lang_id, m,))
            morph_analyses = cursor.fetchall()[0][0]
            if morph_analyses is None:
                new_glossed_morphs[i]['other_glosses'] = []
                continue
            for i2, analysis in enumerate(morph_analyses):
                group = f'Morph-specific ({str(i2)})'
                other_glosses.append({'group': group, 'glosses': analysis['glossing']})
            new_glossed_morphs[i]['other_glosses'] = other_glosses
        
        return new_glossed_morphs


    new_glossed_morphs = []
    
    for i, morph in enumerate(glossed_morphs):
        
        cursor.execute(open("sql_queries/get_morph_glossing.sql", "r").read(), (lang_id, morph['morph'],))
        independent_glossings = cursor.fetchall()[0][0]
        independent = []
        for ind, ind_morph in enumerate(independent_glossings):
            if ind_morph['glossing'] not in morph['glossings']:
                group = f'Morph-specific ({str(ind)})'
                independent.append({'group': group, 'glosses': ind_morph['glossing']})
        
        new_glossed_morphs.append({k:v for k, v in morph.items() if k!= 'glossings'})
        new_glossed_morphs[i]['picked_glosses'] = morph['glossings'][0]
        new_glossed_morphs[i]['other_glosses'] = []
        for ind, analysis in enumerate(morph['glossings']):
            group = f'Unit-specific ({str(ind)})'
            new_glossed_morphs[i]['other_glosses'].append({'group': group, 'glosses': analysis})
        new_glossed_morphs[i]['other_glosses'].extend(independent)
        print()
    
    return new_glossed_morphs

test_input = {'lang_id': 49, 'units': {'0': {'lemma': 'dober', 'pos': 'A', 'realization': 'dober-0', 'unit': 'dober', 'n': 1}, '1': {'lemma': 'dan', 'pos': 'N', 'realization': 'dan-0', 'unit': 'dan', 'n': 2}, '2': {'n': 3, 'unit': 'no', 'realization': 'no', 'lemma': 'no', 'pos': ''}}}

# {
#     'lang_id': 49, 
#     'units': {
#         '0': {
#             'n': 1, 
#             'unit': 'da', 
#             'realization': 'da', 
#             'lemma': 'da', 
#             'pos': ''
#             }
#             }
#             }

def multiple_units(client_input: dict):
    lang_id = client_input['lang_id']
    units = [v for v in client_input['units'].values()]
    for_export = []
    for unit in units:
        for_export.extend(
            export_glossing(
                lang_id, unit['unit'], unit['realization']
                )
            )
    return for_export



# result = export_glossing(49, 'nov', 'nov-0')
# result = multiple_glosses(test_input)
# print(result)