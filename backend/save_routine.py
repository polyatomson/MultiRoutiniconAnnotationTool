import config
import psycopg2
from markupsafe import escape
import json
import re

conn = psycopg2.connect(database=config.DATABASE,
                        host=config.DB_HOST,
                        user=config.DB_USER,
                        password=config.DB_PASSWORD,
                        port=config.DB_PORT)
conn.set_session(autocommit=True)
cursor = conn.cursor()

test = [{'routine': 'da', 
         'lang': 'si', 
         'exprs': [{'expr_full': 'daj no', 'expr_id': 280, 'glossing': 'give-2.IMP.SG PART', 'lang': 'si', 'lemmas': 'dati no', 'pos': 'V PART', 'realization': 'da-j no'}, {'expr_full': 'dan', 'expr_id': 222, 'glossing': 'day-NOM/ACC.SG', 'lang': 'si', 'lemmas': 'dan', 'pos': 'N', 'realization': 'dan-0'}], 
         'situation_structure': 'reaction + prompt', 'pragmatics': ['cry of distress', 'summoning'], 'sit_tags': ['accident', 'danger'], 'situations': {'effect': ['help [a]'], 'trigger': ['danger']}, 'usage_conditions': [{'category': 'relationship', 'condition': 'The speaker is not addressing any specific person. ', 'condition_id': '99'}], 
         'frame_id': 31, 'definition': '', 'comments': '', 'intonation': ''}
         ]

test2 = [
    {
        "routine": "ak",
        "lang": "si",
        "exprs": [
            {
                "expr_full": "daj",
                "expr_id": 304,
                "glossing": "give-2.IMP.SG",
                "lang": "si",
                "lemmas": "dati",
                "pos": "V",
                "realization": "da-j"
            }
        ],
        "situation_structure": "reaction + prompt",
        "pragmatics": [
            "cry of distress",
            "summoning"
        ],
        "sit_tags": [
            "accident",
            "danger"
        ],
        "situations": {
            "effect": [
                "help [a]"
            ],
            "trigger": [
                "danger"
            ]
        },
        "usage_conditions": [
            {
                "category": "relationship",
                "condition": "The speaker is not addressing any specific person. ",
                "condition_id": "99"
            }
        ],
        "frame_id": 31,
        "definition": "",
        "comments": "",
        "intonation": "",
        "examples": [
            {
                "example_id": 1,
                "example": "W",
                "source": "InterCorp-16",
                "translation": "T"
            },
            {
                "example_id": 2,
                "example": "B",
                "source": "InterCorp-16",
                "translation": "Tb"
            }
        ]
    },
    {
        "routine": "da",
        "lang": "si",
        "exprs": [
            {
                "expr_full": "daj",
                "expr_id": 304,
                "glossing": "give-2.IMP.SG",
                "lang": "si",
                "lemmas": "dati",
                "pos": "V",
                "realization": "da-j"
            }
        ],
        "situation_structure": "reaction + prompt",
        "pragmatics": [
            "cry of distress"
        ],
        "sit_tags": [
            "accident",
            "danger"
        ],
        "situations": {
            "effect": [
                "leaving [A]"
            ],
            "trigger": [
                "danger"
            ]
        },
        "usage_conditions": [
            {
                "category": "relationship",
                "condition": "The speaker is not addressing any specific person. ",
                "condition_id": "99"
            }
        ],
        "frame_id": 33,
        "definition": "",
        "comments": "",
        "intonation": "",
        "examples": []
    }
]
def save_routine(data: dict) -> dict[str, int]:
    print(data)
    # general info
    routine = data['routine']
    lang = data['lang']
    expr_ids = [exp['expr_id'] for exp in data['exprs']]
    try:
        cursor.execute("""
                            with r_id as (
                            insert into routines (lang_id, "routine") values((select l.lang_id from langs l where lang = %s), %s) returning routine_id),
                            cj as (select routine_id, expr_id from r_id cross join unnest(%s) expr_id) 
                            insert into routines2expressions (routine_id, expr_id) select * from cj returning routine_id;""",
                            (lang, routine, expr_ids))
        routine_id = cursor.fetchone()[0]
        conn.commit()
    except Exception as ex:
        if ex.pgcode == '23505':
            return {'routine_id': None, 'problem': str(ex)}
        else:
            raise

    # routines2frames
    stripifstr = lambda x: x.strip() if type(x) == str else x
    nullify = lambda x: None if str(x).strip() == '' else stripifstr(x)
    prepared = (routine_id, data['frame_id'], nullify(data['definition']), nullify(data['intonation']), nullify(data['comments']))
    cursor.execute("""INSERT INTO routines2frames (routine_id, frame_id, definition, intonation, comments)
                       values(%s, %s, %s, %s, %s)
                   """, prepared)
    conn.commit()

    if data['examples'] != []:
        examples = (routine_id, data['frame_id'], json.dumps([exobj for exobj in data['examples'] if nullify(exobj['example']) is not None]))
    # print(examples)
        cursor.execute(
            """
                with inp_data as (select %s a, %s b, %s c),
                r2f_id as (select rf.routines2frames_id from routines2frames rf, inp_data where rf.routine_id = inp_data.a and rf.frame_id = inp_data.b),
                ex_unnested as (select jsonb_array_elements(c::jsonb) c from inp_data)
                insert into examples(routines2frames_id, example, ex_source, "translation") select r2f_id.routines2frames_id, eu.c ->> 'example' e, eu.c ->> 'source' s, eu.c ->> 'translation' t from ex_unnested eu, r2f_id;
            """, examples
        )

    if data['cxs'] != []:
        print('cxs to save')
        cursor.executemany("""
                insert into routines2cxs(routine_id, cx_id) values (%s, %s)
            """, [(routine_id, cx_id) for cx_id in data['cxs']])
        if data['cx_examples'] != {}:
            for cx_id, cx_examples in data['cx_examples'].items():
                cursor.executemany("""
                        insert into examples4cxs (routine_id, cx_id, example, ex_source, translation, dated) 
                                   values (%s, %s, %s, %s, %s, %s)
                """, [(routine_id, cx_id, ex['cx_example'], 
                       nullify(ex['source']), nullify(ex['translation']), ex['dated'])
                       for ex in cx_examples])
        if data['cx_reductions'] != {}:
            for cx_id, cx_reductions in data['cx_reductions'].items():
                cursor.executemany("""
                                   insert into cx_reductions(routine_id, cx_id, change, component, sem_role)
                                   values (%s, %s, %s, %s, %s)
                                   """, [(routine_id, cx_id, r['change'], r['component'], nullify(r['sem_role'])
                                    ) for r in cx_reductions])
    return {'routine_id': routine_id}

# save_routine(test2)