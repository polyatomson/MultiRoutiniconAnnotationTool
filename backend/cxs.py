import config
import psycopg2
import json
import re
from markupsafe import escape

conn = psycopg2.connect(database=config.DATABASE,
                        host=config.DB_HOST,
                        user=config.DB_USER,
                        password=config.DB_PASSWORD,
                        port=config.DB_PORT)
conn.set_session(autocommit=True)
cursor = conn.cursor()

def all_cxs() -> list[dict]:
    cursor.execute("""SELECT jsonb_agg(t) FROM (SELECT * FROM all_constructions ac LEFT JOIN langs l on (l.lang_id = ac.lang_id) order by l.lang, cx_id) t;""")
    return cursor.fetchone()[0]

def cx_info(cx_id) -> list[dict]:
    cursor.execute("""SELECT all_routines FROM all_constructions ac where cx_id = %s;""", (cx_id, ))
    return cursor.fetchone()[0]

def cx_table() -> list[dict]:
    cursor.execute("""SELECT jsonb_agg(t) FROM 
                   (SELECT l.lang, c.lang_id, c.cx_id, c.cx_formula, c.syntactic_type, c.cx_semantics 
                   FROM constructions c LEFT JOIN langs l ON c.lang_id = l.lang_id order by l.lang, cx_id) t""")
    return cursor.fetchone()[0]

def add_cx(cx: dict) -> dict[str, int]:
    stripifstr = lambda x: x.strip() if type(x) == str else x
    nullify = lambda x: None if str(x).strip() == '' else stripifstr(x)
    cx = {k:nullify(v) for k,v in cx.items()}
    print(cx)
    if cx['cx_formula'] is None:
        print(cx)
        return {'allgood': False, 'problem': 'The formula cannot be null'}
    try:
        cursor.execute(
            """
    insert into constructions (lang_id, cx_formula, cx_semantics, syntactic_type)
    select (dat ->> 'lang_id')::integer lang_id, dat ->> 'cx_formula' cx_formula, dat ->> 'cx_semantics' cx_semantics, dat ->> 'syntactic_type' syntactic_type 
    from (select %s::jsonb dat) returning cx_id
        """, (json.dumps(cx), )
        )
        cx_id = cursor.fetchone()[0]
        return {'cx_id': cx_id, 'allgood': True}
    except Exception as ex:
        if ex.pgcode == '23505':
            problem = re.findall(r'DETAIL:  (.*?)\n', ex.pgerror)[0]
            return {'allgood': False, 'problem': problem}

def update_cx(cx: dict) -> dict[str, int]:
    stripifstr = lambda x: x.strip() if type(x) == str else x
    nullify = lambda x: None if str(x).strip() == '' else stripifstr(x)
    cx = {k:nullify(v) for k,v in cx.items()}
    print(cx)
    if cx['cx_formula'] is None:
        print(cx)
        return {'allgood': False, 'problem': 'The formula cannot be null'}
    try:
        cursor.execute(
            """
    update constructions set cx_formula = %s, cx_semantics = %s, syntactic_type = %s
    where cx_id = %s
        """, (cx['cx_formula'], cx['cx_semantics'], cx['syntactic_type'], cx['cx_id']))
        return {'allgood': True}
    except Exception as ex:
        if ex.pgcode == '23505':
            problem = re.findall(r'DETAIL:  (.*?)\n', ex.pgerror)[0]
            return {'allgood': False, 'problem': problem}

def get_reductions() -> dict[str, list]:
    cursor.execute("""
                   select jsonb_agg(t) from (
                    with changes as (select jsonb_agg(distinct cr."change") changes from cx_reductions cr where cr.change is not null),

                    elements as (select jsonb_agg(distinct cr.component) components from cx_reductions cr where cr.component is not null),

                    sem_roles as (select jsonb_agg(distinct cr.sem_role) sem_roles from cx_reductions cr where cr.sem_role is not null)

                    select c.changes, e.components, s.sem_roles from changes c, elements e, sem_roles s) t;
                """)
    return cursor.fetchone()[0][0]

def rereference_cxs(routine_id: int, cx_ids: list[int]) -> dict[str, str]:
    cursor.execute("""SELECT cx_id FROM routines2cxs WHERE routine_id=%s;""", (routine_id,))
    cx_ids_db = [cx_id[0] for cx_id in cursor.fetchall()]
    to_remove = [cx_id for cx_id in cx_ids_db if cx_id not in cx_ids]
    to_add = [cx_id for cx_id in cx_ids if cx_id not in cx_ids_db]
    status = {}
    if to_add != []:
        cursor.executemany("""INSERT INTO routines2cxs (cx_id, routine_id) VALUES (%s, %s)""", 
                       [(cx_id, routine_id) for cx_id in to_add])
        status['n_added'] = cursor.rowcount
    if to_remove != []:
        cursor.executemany("""
                           WITH rm_red as (DELETE FROM cx_reductions where cx_id = %(cx_id)s and routine_id = %(routine_id)s),
                           rm_ex as (DELETE FROM examples4cxs where cx_id = %(cx_id)s and routine_id = %(routine_id)s)
                           DELETE FROM routines2cxs WHERE cx_id = %(cx_id)s AND routine_id = %(routine_id)s""",
                       [{'cx_id': cx_id, 'routine_id': routine_id} for cx_id in to_remove])
        status['n_deleted'] = cursor.rowcount
    conn.commit()
    return status

def change_info(routine_id: int, cx_example_list: list[dict], reduction_list: list[dict]) -> dict:
    notempty = lambda x: False if x is None or x.strip() == '' else True
    new_reds = [red for red in reduction_list if 'reduction_id' not in red]
    upd_reds = [red for red in reduction_list if 'reduction_id' in red]
    new_exs = [ex for ex in cx_example_list if 'example_id' not in ex]
    upd_exs = [ex for ex in cx_example_list if 'example_id' in ex]
    
    cursor.execute("""select reduction_id from cx_reductions where routine_id = %s""", (routine_id, ))
    existing_red_ids = [red[0] for red in cursor.fetchall()]
    cursor.execute("""select example4cx_id from examples4cxs where routine_id = %s""", (routine_id, ))
    existing_ex_ids = [ex[0] for ex in cursor.fetchall()]
    keep_red_ids = [red['reduction_id'] for red in upd_reds]
    del_reds = [red_id for red_id in existing_red_ids if red_id not in keep_red_ids ]
    keep_ex_ids = [ex['example_id'] for ex in upd_exs]
    del_exs = [ex_id for ex_id in existing_ex_ids if ex_id not in keep_ex_ids ]
    
    # delete old (by ids)
    if del_reds != []:
        cursor.execute("""
                   delete from cx_reductions where reduction_id = any(%s)
                   """, (del_reds, ))
    if del_exs != []:
        cursor.execute("""
                   delete from examples4cxs where example4cx_id = any(%s)
                   """, (del_exs, ))
    # update old
    if upd_reds != []:
        cursor.execute("""
                   with dat as (
                   select jsonb_array_elements(%s::jsonb) ex),

                dat_prep as (select 
                    (ex ->> 'reduction_id')::integer reduction_id, 
                    (ex ->> 'change') change,
                    (ex ->> 'component') component, 
                    ex ->> 'sem_role' sem_role
                    from dat)

                update cx_reductions main 
                   set 
                    change = dat_prep.change, 
                    component = dat_prep.component, 
                    sem_role = dat_prep.sem_role
                from dat_prep
                where main.reduction_id = dat_prep.reduction_id;
                """, (json.dumps(upd_reds), ))
    if upd_exs != []:
        cursor.execute("""
                   with dat as (
                   select jsonb_array_elements(%s::jsonb) ex),

                dat_prep as (select 
                    (ex ->> 'example_id')::integer example4cx_id, 
                    (ex ->> 'example') example,
                    (ex ->> 'dated')::integer dated, 
                    ex ->> 'source' ex_source, 
                    ex ->> 'translation' "translation"
                    from dat)

                update examples4cxs main 
                   set 
                    example = dat_prep.example, 
                    ex_source = dat_prep.ex_source, 
                    dated = dat_prep.dated,
                    "translation" = dat_prep."translation"
                from dat_prep
                where main.example4cx_id = dat_prep.example4cx_id;
                """, (json.dumps(upd_exs), ))
    # insert new
    if new_reds != []:
        cursor.execute("""
                   with dat as (
                   select jsonb_array_elements(%s::jsonb) ex, %s routine_id),

                insert into cx_reductions (
                   cx_id, routine_id, change, component, sem_role)
                   
                   select 
                    (ex ->> 'cx_id')::integer cx_id,
                    routine_id,
                    (ex ->> 'change') change,
                    (ex ->> 'component') component, 
                    ex ->> 'sem_role' sem_role
                   
                    from dat
                """, (json.dumps(new_reds), routine_id))
    if new_exs != []:
        cursor.execute("""
                   with dat as (
                   select jsonb_array_elements(%s::jsonb) ex, %s routine_id),

                insert into examples4cxs (
                   cx_id, routine_id, example, ex_source, 
                   "translation", dated)
                select 
                    (ex ->> 'cx_id')::integer cx_id, 
                    routine_id,
                    (ex ->> 'example') example,
                    ex ->> 'source' ex_source, 
                    ex ->> 'translation' "translation"
                    (ex ->> 'dated')::integer dated, 
                    
                   from dat;
                """, (json.dumps(new_exs), routine_id))
    
    return {'status': 'ok'}

test_cx_ex = [
  {
    "cx_id": 42,
    "dated": 2000,
    "example": "c",
    "example_id": 3,
    "source": None,
    "translation": None
  }
]
test_red = [
  {
    "cx_id": 42,
    "change": "a",
    "component": "e",
    "reduction_id": 7,
    "sem_role": None
  }
]

# test = {"cx_id": 23, "lang": "ru", "lang_id": 58, "cx_semantics": "a", "syntactic_type": "nominal", "cx_formula": "ничего A-Gen.Sg.N"}
# add_cx(test)
# update_cx(test)
change_info(48, test_cx_ex, test_red)