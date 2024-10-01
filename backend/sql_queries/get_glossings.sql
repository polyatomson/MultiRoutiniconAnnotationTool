select jsonb_agg(t) from
( select s.unit, s.morph, s.n, 
array_agg(s.glossing) as glossings
from
   
   (select u.unit as unit, u.unit_id as unit_id, m.morph as morph, 
   u2m.place as n, 
   json_agg(json_build_object(
      'gloss_value', 
      (CASE WHEN g.lex = false THEN UPPER(g.gloss)
         ELSE LOWER(g.gloss)
         END), 'gloss_id', g.gloss_id)) as glossing
   from public.units u
   natural join public.units2morphs u2m
   natural join public.morphs m
   natural join public.morph2glosses m2g
   natural join public.glosses g
   
   where u.lang_id = %s and u.realization = %s

   group by u.unit, u2m.place, u.unit_id, m.morph_id, m.morph
   order by u2m.place asc) s
   
   group by s.unit, s.morph, s.n
   order by s.n
   ) t