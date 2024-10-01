select jsonb_agg(t) from

   (select m.morph as morph, m.morph_id, 
   json_agg(json_build_object(
      'gloss_value', 
      (CASE WHEN g.lex = false THEN UPPER(g.gloss)
         ELSE LOWER(g.gloss)
         END), 'gloss_id', g.gloss_id)) as glossing
   from public.morphs m
   natural join public.morph2glosses m2g
   natural join public.glosses g
   
   where m.lang_id = %s and m.morph = %s

   group by m.morph_id, m.morph) t