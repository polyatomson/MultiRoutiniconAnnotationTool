select json_agg(res) from

(select t3.lang, 
jsonb_agg(json_build_object(
	'expression', t3.expr_full,
	'expression_id', t3.expr_id,
	'pos', t3.pos,
	'lemmas', t3.lemmas,
	'realization', t3.realization,
	'glossing', t3.glossing
)) entries

from
(select t2.lang lang, t2.expr_full, t2.expr_id,
string_agg(t2.lemma, ' ' order by t2.unit_place) lemmas, 
string_agg(t2.pos, ' ' order by t2.unit_place) pos, 
string_agg(t2.realization, ' ' order by t2.unit_place) realization,
string_agg(t2.glosses, ' ' order by t2.unit_place) glossing

from

(select t1.lang lang, t1.expr_id, t1.expr_full, t1.lemma, t1.pos, t1.realization, t1.unit_id, t1.unit_place, string_agg(t1.glosses, '-' order by t1.morph_place) glosses
from
(
select l.lang, e.expr_full, e.expr_id, u.unit_id, eu.place unit_place, um.place morph_place, m.morph, u.lemma, u.pos, u.realization, string_agg(m.glosses, '\') glosses 
from expressions e
left join langs l on (e.lang_id=l.lang_id)
left join expressions2units eu on (e.expr_id=eu.expr_id)
left join units u on (eu.unit_id=u.unit_id)
left join units2morphs um on (u.unit_id=um.unit_id)
left join morphs m	on (um.morph_id=m.morph_id)
group by l.lang , e.expr_full, u.unit_id, eu.place, u.lemma, u.pos, u.realization, e.expr_id, m.morph, um.place
) t1
group by t1.lang, t1.expr_full, t1.lemma, t1.pos, t1.realization, t1.unit_id, t1.unit_place, t1.expr_id) t2

group by t2.lang, t2.expr_full, t2.expr_id) t3

group by t3.lang) res