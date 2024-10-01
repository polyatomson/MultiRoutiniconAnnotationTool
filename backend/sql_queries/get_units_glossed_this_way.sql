select json_agg(fin) from (select distinct t2.lang, t2.unit_id, t2.unit, t2.glossing  from

(select t.lang, t.unit, t.unit_id, t.res as glossing, json_array_elements(json_array_elements(t.gl_ids)) as unnested

from

	(SELECT s.lang,
	s.unit,
	    s.unit_id,
	    jsonb_agg(s.glossed_morph order by s.place) as res,
	    json_agg(s.gl_ids) as gl_ids
	    
	   FROM ( SELECT l.lang,
	   			u.unit,
	            u.unit_id,
	            jsonb_build_object('morph',m.morph, 'glossed', 
				jsonb_agg(
					CASE WHEN g.lex = false THEN UPPER(g.gloss)
         			ELSE LOWER(g.gloss)
         			END
					order by (case when g.lex=false then 2 else 1 end))) as glossed_morph,
	            json_agg(g.gloss_id) as gl_ids,
	            u2m.place
	           FROM units u
	           join langs l using (lang_id)
	             JOIN units2morphs u2m USING (unit_id)
	             JOIN morphs m USING (lang_id, morph_id)
	             JOIN morph2glosses m2g USING (morph_id)
	             JOIN glosses g USING (gloss_id)
	          
	          GROUP BY l.lang, u.unit, u2m.place, u.unit_id, m.morph_id, m.morph
	          ORDER BY u.unit, u2m.place) s
	          
	  GROUP BY lang, unit, unit_id) t) t2
	  
where t2.unnested::text = %s) fin