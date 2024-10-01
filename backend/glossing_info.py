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

def glossing_examples(gl_id: int) -> dict[list[dict]]:
    cursor.execute("""
        
                   select jsonb_agg(t) from (
                   
        with uids as (
        select distinct u.unit_id, u.unit, u.lang_id from 
        units u left join units2morphs um on u.unit_id = um.unit_id
        left join morph2glosses mg on um.morph_id = mg.morph_id 
        left join morphs m on mg.morph_id = m.morph_id 
        left join glosses g on mg.gloss_id = g.gloss_id
        where mg.gloss_id = %s), 

        gl_m as (

        select m.morph_id, m.morph, string_agg(case when g.lex=true then g.gloss else upper(g.gloss) end, '.' order by g.lex desc, g.gloss asc) gl
        from
        morphs m 
        left join morph2glosses mg on m.morph_id = mg.morph_id
        left join glosses g on mg.gloss_id = g.gloss_id
        group by m.morph_id, m.morph
        )

        select uids.unit_id, uids.unit, uids.lang_id, l.lang, jsonb_build_object('morphs', jsonb_agg(gl_m.morph order by um.place), 'glosses', jsonb_agg(gl_m.gl order by um.place)) glossing
        from uids 
        left join units2morphs um on uids.unit_id = um.unit_id
        left join gl_m on um.morph_id = gl_m.morph_id
        left join langs l on l.lang_id = uids.lang_id
        group by uids.unit_id, uids.unit, uids.lang_id, l.lang
                   order by l.lang
                   ) t
            """, (gl_id, ))
    res = cursor.fetchone()
    if res is None:
        return {'glossing_examples': None}
    else:
        # print(type(res))
        return {'glossing_examples': res[0]}
    
def get_lang_stats(gl_id: int) -> dict[str, list]:
    cursor.execute("""
        with stats as (select l.lang, count(um.unit_id) stats
        from units2morphs um
        left join morph2glosses mg on um.morph_id = mg.morph_id
        left join morphs m on mg.morph_id = m.morph_id
        left join langs l on m.lang_id = l.lang_id
        where mg.gloss_id=%s
        group by l.lang)

        select jsonb_agg(t) from (select jsonb_agg(lang) labels, jsonb_agg(stats) data from stats) t
                   """, (gl_id, ))
    res = cursor.fetchone()
    if res is None:
        return {'labels': None, 'data': None}
    else:
        return res[0][0]

get_lang_stats(973)
# glossing_examples(973)