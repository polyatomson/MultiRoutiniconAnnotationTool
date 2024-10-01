-- DROP SCHEMA public;

CREATE SCHEMA IF NOT EXISTS public AUTHORIZATION pg_database_owner;

-- DROP SEQUENCE public.conditions_condition_id_seq;

CREATE SEQUENCE IF NOT EXISTS public.conditions_condition_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.constructions_cx_id_seq;

CREATE SEQUENCE IF NOT EXISTS public.constructions_cx_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.events_event_id_seq;

CREATE SEQUENCE IF NOT EXISTS public.events_event_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.examples_example_id_seq;

CREATE SEQUENCE IF NOT EXISTS public.examples_example_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.expressions_expr_id_seq;

CREATE SEQUENCE IF NOT EXISTS public.expressions_expr_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.frames_frame_id_seq;

CREATE SEQUENCE IF NOT EXISTS public.frames_frame_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.glosses_gloss_id_seq;

CREATE SEQUENCE IF NOT EXISTS public.glosses_gloss_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.langs_lang_id_seq;

CREATE SEQUENCE IF NOT EXISTS public.langs_lang_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.lemmas_lemma_id_seq;

CREATE SEQUENCE IF NOT EXISTS public.lemmas_lemma_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.morphs_morph_id_seq;

CREATE SEQUENCE IF NOT EXISTS public.morphs_morph_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.pragmatics_pragmatics_id_seq;

CREATE SEQUENCE IF NOT EXISTS public.pragmatics_pragmatics_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.routines2frames_routines2frames_id_seq;

CREATE SEQUENCE IF NOT EXISTS public.routines2frames_routines2frames_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.routines_routine_id_seq;

CREATE SEQUENCE IF NOT EXISTS public.routines_routine_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.situation_tags_st_id_seq;

CREATE SEQUENCE IF NOT EXISTS public.situation_tags_st_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.units_unit_id_seq;

CREATE SEQUENCE IF NOT EXISTS public.units_unit_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;-- public.conditions definition

-- Drop table

-- DROP TABLE public.conditions;

CREATE TABLE IF NOT EXISTS public.conditions (
	condition_id int4 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE) NOT NULL,
	category varchar NULL,
	"condition" varchar NOT NULL,
	CONSTRAINT conditions_pk PRIMARY KEY (condition_id),
	CONSTRAINT conditions_unique UNIQUE (condition)
);


-- public.events definition

-- Drop table

-- DROP TABLE public.events;

CREATE TABLE IF NOT EXISTS public.events (
	event_id int4 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE) NOT NULL,
	"event" varchar NOT NULL,
	CONSTRAINT events_pk PRIMARY KEY (event_id),
	CONSTRAINT events_unique UNIQUE (event)
);


-- public.frames definition

-- Drop table

-- DROP TABLE public.frames;

CREATE TABLE IF NOT EXISTS public.frames (
	frame_id int4 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE) NOT NULL,
	situation_structure varchar NOT NULL,
	unique_code varchar NULL,
	CONSTRAINT frames_pk PRIMARY KEY (frame_id),
	CONSTRAINT frames_unique UNIQUE (unique_code)
);


-- public.glosses definition

-- Drop table

-- DROP TABLE public.glosses;

CREATE TABLE IF NOT EXISTS public.glosses (
	gloss_id int4 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE) NOT NULL,
	gloss varchar NOT NULL,
	lex bool DEFAULT true NULL,
	"class" varchar NULL,
	useless bool DEFAULT false NOT NULL,
	CONSTRAINT glosses_pk PRIMARY KEY (gloss_id),
	CONSTRAINT glosses_un UNIQUE (gloss, useless, lex)
);


-- public.langs definition

-- Drop table

-- DROP TABLE public.langs;

CREATE TABLE IF NOT EXISTS public.langs (
	lang_id int4 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE) NOT NULL,
	lang varchar NOT NULL,
	CONSTRAINT langs_pk PRIMARY KEY (lang_id),
	CONSTRAINT langs_un UNIQUE (lang)
);


-- public.pragmatics definition

-- Drop table

-- DROP TABLE public.pragmatics;

CREATE TABLE IF NOT EXISTS public.pragmatics (
	pragmatics_id int4 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE) NOT NULL,
	pragmatics varchar NOT NULL,
	CONSTRAINT pragmatics_pk PRIMARY KEY (pragmatics_id),
	CONSTRAINT pragmatics_unique UNIQUE (pragmatics)
);


-- public.situation_tags definition

-- Drop table

-- DROP TABLE public.situation_tags;

CREATE TABLE IF NOT EXISTS public.situation_tags (
	st_id int4 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE) NOT NULL,
	situation_tag varchar NOT NULL,
	CONSTRAINT situation_tags_pk PRIMARY KEY (st_id),
	CONSTRAINT situation_tags_unique UNIQUE (situation_tag)
);


-- public.constructions definition

-- Drop table

-- DROP TABLE public.constructions;

CREATE TABLE IF NOT EXISTS public.constructions (
	cx_id int4 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE) NOT NULL,
	cx_formula varchar NOT NULL,
	cx_semantics varchar NULL,
	"syntactic type" varchar NULL,
	lang_id int4 NOT NULL,
	CONSTRAINT constructions_pk PRIMARY KEY (cx_id),
	CONSTRAINT constructions_unique UNIQUE (lang_id, cx_formula, cx_semantics),
	CONSTRAINT constructions_langs_fk FOREIGN KEY (lang_id) REFERENCES public.langs(lang_id)
);


-- public.expressions definition

-- Drop table

-- DROP TABLE public.expressions;

CREATE TABLE IF NOT EXISTS public.expressions (
	expr_id int4 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE) NOT NULL,
	expr_full varchar NOT NULL,
	lang_id int4 NOT NULL,
	"style" varchar NULL,
	CONSTRAINT expressions_pk PRIMARY KEY (expr_id),
	CONSTRAINT expressions_un UNIQUE (expr_full, lang_id),
	CONSTRAINT expressions_fk FOREIGN KEY (lang_id) REFERENCES public.langs(lang_id)
);


-- public.frames2conditions definition

-- Drop table

-- DROP TABLE public.frames2conditions;

CREATE TABLE IF NOT EXISTS public.frames2conditions (
	frame_id int4 NOT NULL,
	condition_id int4 NOT NULL,
	CONSTRAINT frames2conditions_unique UNIQUE (frame_id, condition_id),
	CONSTRAINT frames2conditions_conditions_fk FOREIGN KEY (condition_id) REFERENCES public.conditions(condition_id),
	CONSTRAINT frames2conditions_frames_fk FOREIGN KEY (frame_id) REFERENCES public.frames(frame_id)
);


-- public.frames2events definition

-- Drop table

-- DROP TABLE public.frames2events;

CREATE TABLE IF NOT EXISTS public.frames2events (
	frame_id int4 NOT NULL,
	event_id int4 NOT NULL,
	stage varchar NOT NULL,
	CONSTRAINT frames2events_unique UNIQUE (event_id, frame_id, stage),
	CONSTRAINT frames2events_events_fk FOREIGN KEY (event_id) REFERENCES public.events(event_id),
	CONSTRAINT frames2events_frames_fk FOREIGN KEY (frame_id) REFERENCES public.frames(frame_id)
);


-- public.frames2pragmatics definition

-- Drop table

-- DROP TABLE public.frames2pragmatics;

CREATE TABLE IF NOT EXISTS public.frames2pragmatics (
	frame_id int4 NOT NULL,
	pragmatics_id int4 NOT NULL,
	CONSTRAINT frames2pragmatics_unique UNIQUE (frame_id, pragmatics_id),
	CONSTRAINT frames2pragmatics_frames_fk FOREIGN KEY (frame_id) REFERENCES public.frames(frame_id),
	CONSTRAINT frames2pragmatics_pragmatics_fk FOREIGN KEY (pragmatics_id) REFERENCES public.pragmatics(pragmatics_id)
);


-- public.frames2st definition

-- Drop table

-- DROP TABLE public.frames2st;

CREATE TABLE IF NOT EXISTS public.frames2st (
	frame_id int4 NOT NULL,
	st_id int4 NOT NULL,
	CONSTRAINT frames2st_unique UNIQUE (frame_id, st_id),
	CONSTRAINT frames2st_frames_fk FOREIGN KEY (frame_id) REFERENCES public.frames(frame_id),
	CONSTRAINT frames2st_situation_tags_fk FOREIGN KEY (st_id) REFERENCES public.situation_tags(st_id)
);


-- public.morphs definition

-- Drop table

-- DROP TABLE public.morphs;

CREATE TABLE IF NOT EXISTS public.morphs (
	morph_id int4 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE) NOT NULL,
	morph varchar NOT NULL,
	lang_id int4 NOT NULL,
	glosses varchar NULL,
	CONSTRAINT morphs_pk PRIMARY KEY (morph_id),
	CONSTRAINT morphs_un UNIQUE (morph, lang_id, glosses),
	CONSTRAINT morphs_langs_fk FOREIGN KEY (lang_id) REFERENCES public.langs(lang_id)
);


-- public."routines" definition

-- Drop table

-- DROP TABLE public."routines";

CREATE TABLE IF NOT EXISTS public."routines" (
	routine_id int4 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE) NOT NULL,
	"routine" varchar NOT NULL,
	lang_id int4 NOT NULL,
	CONSTRAINT routines_pk PRIMARY KEY (routine_id),
	CONSTRAINT routines_unique UNIQUE (routine, lang_id),
	CONSTRAINT routines_langs_fk FOREIGN KEY (lang_id) REFERENCES public.langs(lang_id)
);


-- public.routines2cxs definition

-- Drop table

-- DROP TABLE public.routines2cxs;

CREATE TABLE IF NOT EXISTS public.routines2cxs (
	routine_id int4 NOT NULL,
	cx_id int4 NOT NULL,
	shift varchar NULL,
	CONSTRAINT routines2cxs_check CHECK ((((shift)::text ~~ ('reduction of'::text || '%'::text)) OR ((shift)::text = 'no reduction'::text))),
	CONSTRAINT routines2cxs_pk PRIMARY KEY (routine_id, cx_id),
	CONSTRAINT routines2cxs_constructions_fk FOREIGN KEY (cx_id) REFERENCES public.constructions(cx_id),
	CONSTRAINT routines2cxs_routines_fk FOREIGN KEY (routine_id) REFERENCES public."routines"(routine_id)
);


-- public.routines2expressions definition

-- Drop table

-- DROP TABLE public.routines2expressions;

CREATE TABLE IF NOT EXISTS public.routines2expressions (
	routine_id int4 NOT NULL,
	expr_id int4 NOT NULL,
	CONSTRAINT routines2expressions_unique UNIQUE (routine_id, expr_id),
	CONSTRAINT routines2expressions_expressions_fk FOREIGN KEY (expr_id) REFERENCES public.expressions(expr_id),
	CONSTRAINT routines2expressions_routines_fk FOREIGN KEY (routine_id) REFERENCES public."routines"(routine_id)
);


-- public.routines2frames definition

-- Drop table

-- DROP TABLE public.routines2frames;

CREATE TABLE IF NOT EXISTS public.routines2frames (
	routines2frames_id int4 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE) NOT NULL,
	routine_id int4 NOT NULL,
	frame_id int4 NOT NULL,
	definition varchar NULL,
	"comments" varchar NULL,
	intonation varchar NULL,
	CONSTRAINT routines2frames_pk PRIMARY KEY (routines2frames_id),
	CONSTRAINT routines2frames_unique UNIQUE (routine_id, frame_id),
	CONSTRAINT fk_frame_id FOREIGN KEY (frame_id) REFERENCES public.frames(frame_id),
	CONSTRAINT fk_routine_id FOREIGN KEY (routine_id) REFERENCES public."routines"(routine_id)
);


-- public.units definition

-- Drop table

-- DROP TABLE public.units;

CREATE TABLE IF NOT EXISTS public.units (
	unit_id int4 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE) NOT NULL,
	lang_id int4 NOT NULL,
	unit varchar NOT NULL,
	lemma varchar NULL,
	pos varchar NULL,
	realization varchar NULL,
	glossing varchar NULL,
	CONSTRAINT unitd_unique_new1 UNIQUE (lang_id, unit, lemma, pos, realization, glossing),
	CONSTRAINT units_pk PRIMARY KEY (unit_id),
	CONSTRAINT units_fk FOREIGN KEY (lang_id) REFERENCES public.langs(lang_id)
);


-- public.units2morphs definition

-- Drop table

-- DROP TABLE public.units2morphs;

CREATE TABLE IF NOT EXISTS public.units2morphs (
	unit_id int4 NOT NULL,
	morph_id int4 NOT NULL,
	place int4 NOT NULL,
	CONSTRAINT units2morphs_un UNIQUE (unit_id, morph_id, place),
	CONSTRAINT units2morphs_unique UNIQUE (unit_id, place),
	CONSTRAINT units2morphs_fk FOREIGN KEY (unit_id) REFERENCES public.units(unit_id),
	CONSTRAINT units2morphs_fk_1 FOREIGN KEY (morph_id) REFERENCES public.morphs(morph_id)
);


-- public.examples definition

-- Drop table

-- DROP TABLE public.examples;

CREATE TABLE IF NOT EXISTS public.examples (
	example_id int4 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE) NOT NULL,
	rotines2frames_id int4 NOT NULL,
	example varchar NOT NULL,
	CONSTRAINT examples_pk PRIMARY KEY (example_id),
	CONSTRAINT examples_unique UNIQUE (example),
	CONSTRAINT examples_routines2frames_fk FOREIGN KEY (rotines2frames_id) REFERENCES public.routines2frames(routines2frames_id)
);


-- public.expressions2units definition

-- Drop table

-- DROP TABLE public.expressions2units;

CREATE TABLE IF NOT EXISTS public.expressions2units (
	expr_id int4 NOT NULL,
	unit_id int4 NOT NULL,
	place int4 NOT NULL,
	CONSTRAINT expressions2units_un UNIQUE (expr_id, unit_id, place),
	CONSTRAINT expressions2units_fk FOREIGN KEY (expr_id) REFERENCES public.expressions(expr_id),
	CONSTRAINT expressions2units_fk_1 FOREIGN KEY (unit_id) REFERENCES public.units(unit_id)
);


-- public.morph2glosses definition

-- Drop table

-- DROP TABLE public.morph2glosses;

CREATE TABLE IF NOT EXISTS public.morph2glosses (
	morph_id int4 NOT NULL,
	gloss_id int4 NOT NULL,
	CONSTRAINT morph2glosses_un UNIQUE (morph_id, gloss_id),
	CONSTRAINT morph2glosses_fk FOREIGN KEY (morph_id) REFERENCES public.morphs(morph_id),
	CONSTRAINT morph2glosses_fk_1 FOREIGN KEY (gloss_id) REFERENCES public.glosses(gloss_id)
);


-- public.all_expressions source

CREATE OR REPLACE VIEW public.all_expressions
AS SELECT lang,
    expr_full,
    expr_id,
    lemmas,
    pos,
    realization,
    glossing
   FROM ( SELECT t2.lang,
            t2.expr_full,
            t2.expr_id,
            string_agg(t2.lemma::text, ' '::text ORDER BY t2.unit_place) AS lemmas,
            string_agg(t2.pos::text, ' '::text ORDER BY t2.unit_place) AS pos,
            string_agg(t2.realization::text, ' '::text ORDER BY t2.unit_place) AS realization,
            string_agg(t2.glosses, ' '::text ORDER BY t2.unit_place) AS glossing
           FROM ( SELECT t1.lang,
                    t1.expr_id,
                    t1.expr_full,
                    t1.lemma,
                    t1.pos,
                    t1.realization,
                    t1.unit_id,
                    t1.unit_place,
                    string_agg(t1.glosses, '-'::text ORDER BY t1.morph_place) AS glosses
                   FROM ( SELECT l.lang,
                            e.expr_full,
                            e.expr_id,
                            u.unit_id,
                            eu.place AS unit_place,
                            um.place AS morph_place,
                            m.morph,
                            u.lemma,
                            u.pos,
                            u.realization,
                            string_agg(m.glosses::text, '\'::text) AS glosses
                           FROM expressions e
                             LEFT JOIN langs l ON e.lang_id = l.lang_id
                             LEFT JOIN expressions2units eu ON e.expr_id = eu.expr_id
                             LEFT JOIN units u ON eu.unit_id = u.unit_id
                             LEFT JOIN units2morphs um ON u.unit_id = um.unit_id
                             LEFT JOIN morphs m ON um.morph_id = m.morph_id
                          GROUP BY l.lang, e.expr_full, u.unit_id, eu.place, u.lemma, u.pos, u.realization, e.expr_id, m.morph, m.morph_id, um.place) t1
                  GROUP BY t1.lang, t1.expr_full, t1.lemma, t1.pos, t1.realization, t1.unit_id, t1.unit_place, t1.expr_id) t2
          GROUP BY t2.lang, t2.expr_full, t2.expr_id) t3;


-- public.all_expressions_with source

CREATE OR REPLACE VIEW public.all_expressions_with
AS WITH glossed_units AS (
         SELECT gl_m.unit_id,
            string_agg(gl_m.morph::text, '-'::text ORDER BY gl_m.place) AS realization,
            string_agg(gl_m.glossed, '-'::text ORDER BY gl_m.place) AS glossed,
            gl_m.lemma,
            gl_m.pos
           FROM ( SELECT u.unit_id,
                    m.morph,
                    um.place,
                    u.lemma,
                    u.pos,
                    string_agg(
                        CASE
                            WHEN g.lex = false THEN upper(g.gloss::text)
                            ELSE lower(g.gloss::text)
                        END, '.'::text ORDER BY (
                        CASE
                            WHEN g.lex = false THEN 2
                            ELSE 1
                        END)) AS glossed
                   FROM units u
                     LEFT JOIN units2morphs um ON u.unit_id = um.unit_id
                     LEFT JOIN morphs m ON um.morph_id = m.morph_id
                     LEFT JOIN morph2glosses mg ON m.morph_id = mg.morph_id
                     LEFT JOIN glosses g ON g.gloss_id = mg.gloss_id
                  GROUP BY u.unit_id, u.realization, m.morph_id, m.morph, um.place, u.lemma, u.pos) gl_m
          GROUP BY gl_m.unit_id, gl_m.pos, gl_m.lemma
        )
 SELECT e.expr_id,
    l.lang,
    e.expr_full,
    string_agg(gu.lemma::text, ' '::text ORDER BY eu.place) AS lemmas,
    string_agg(gu.pos::text, ' '::text ORDER BY eu.place) AS pos,
    string_agg(gu.realization, ' '::text ORDER BY eu.place) AS realization,
    string_agg(gu.glossed, ' '::text ORDER BY eu.place) AS glossing
   FROM expressions e
     LEFT JOIN langs l ON e.lang_id = l.lang_id
     LEFT JOIN expressions2units eu ON e.expr_id = eu.expr_id
     LEFT JOIN glossed_units gu ON gu.unit_id = eu.unit_id
  GROUP BY l.lang, e.expr_id, e.expr_full;


-- public.all_frames source

CREATE OR REPLACE VIEW public.all_frames
AS SELECT DISTINCT frame_id,
    situation_structure,
    pragmatics,
    usage_conditions,
    sit_tags,
    jsonb_agg(stages) AS situations
   FROM ( SELECT f.frame_id,
            f.situation_structure,
            jsonb_agg(DISTINCT p.pragmatics) AS pragmatics,
            jsonb_agg(DISTINCT jsonb_build_object('category', c.category, 'condition', c.condition)) AS usage_conditions,
            jsonb_agg(DISTINCT st.situation_tag) AS sit_tags,
            jsonb_build_object('stage', fe.stage, 'event_type', jsonb_agg(e.event)) AS stages
           FROM frames f
             LEFT JOIN frames2conditions fc ON f.frame_id = fc.frame_id
             LEFT JOIN frames2events fe ON f.frame_id = fe.frame_id
             LEFT JOIN frames2pragmatics fp ON f.frame_id = fp.frame_id
             LEFT JOIN frames2st fs2 ON f.frame_id = fs2.frame_id
             LEFT JOIN conditions c ON fc.condition_id = c.condition_id
             LEFT JOIN events e ON fe.event_id = e.event_id
             LEFT JOIN pragmatics p ON fp.pragmatics_id = p.pragmatics_id
             LEFT JOIN situation_tags st ON fs2.st_id = st.st_id
          GROUP BY f.frame_id, f.situation_structure, fe.stage) t
  GROUP BY frame_id, situation_structure, pragmatics, usage_conditions, sit_tags;


-- public.for_routinicon source

CREATE OR REPLACE VIEW public.for_routinicon
AS SELECT expr_full,
    realization,
    glossing
   FROM ( SELECT t2.lang,
            t2.expr_full,
            t2.expr_id,
            string_agg(t2.lemma::text, ' '::text ORDER BY t2.unit_place) AS lemmas,
            string_agg(t2.pos::text, ' '::text ORDER BY t2.unit_place) AS pos,
            string_agg(t2.realization::text, ' '::text ORDER BY t2.unit_place) AS realization,
            string_agg(t2.glosses, ' '::text ORDER BY t2.unit_place) AS glossing
           FROM ( SELECT t1.lang,
                    t1.expr_id,
                    t1.expr_full,
                    t1.lemma,
                    t1.pos,
                    t1.realization,
                    t1.unit_id,
                    t1.unit_place,
                    string_agg(t1.glosses, '-'::text ORDER BY t1.morph_place) AS glosses
                   FROM ( SELECT l.lang,
                            e.expr_full,
                            e.expr_id,
                            u.unit_id,
                            eu.place AS unit_place,
                            um.place AS morph_place,
                            m.morph,
                            u.lemma,
                            u.pos,
                            u.realization,
                            string_agg(m.glosses::text, '\'::text) AS glosses
                           FROM expressions e
                             LEFT JOIN langs l ON e.lang_id = l.lang_id
                             LEFT JOIN expressions2units eu ON e.expr_id = eu.expr_id
                             LEFT JOIN units u ON eu.unit_id = u.unit_id
                             LEFT JOIN units2morphs um ON u.unit_id = um.unit_id
                             LEFT JOIN morphs m ON um.morph_id = m.morph_id
                          GROUP BY l.lang, e.expr_full, u.unit_id, eu.place, u.lemma, u.pos, u.realization, e.expr_id, m.morph, m.morph_id, um.place) t1
                  GROUP BY t1.lang, t1.expr_full, t1.lemma, t1.pos, t1.realization, t1.unit_id, t1.unit_place, t1.expr_id) t2
          GROUP BY t2.lang, t2.expr_full, t2.expr_id) t3
  WHERE lang::text = 'ru'::text;


-- public.glossed_units source

CREATE OR REPLACE VIEW public.glossed_units
AS SELECT DISTINCT lang,
    unit_id,
    unit,
    glossing
   FROM ( SELECT t.lang,
            t.unit,
            t.unit_id,
            t.res AS glossing,
            json_array_elements(json_array_elements(t.gl_ids)) AS unnested
           FROM ( SELECT s.lang,
                    s.unit,
                    s.unit_id,
                    jsonb_agg(s.glossed_morph ORDER BY s.place) AS res,
                    json_agg(s.gl_ids) AS gl_ids
                   FROM ( SELECT l.lang,
                            u.unit,
                            u.unit_id,
                            jsonb_build_object('morph', m.morph, 'glossed', jsonb_agg(
                                CASE
                                    WHEN g.lex = false THEN upper(g.gloss::text)
                                    ELSE lower(g.gloss::text)
                                END ORDER BY (
                                CASE
                                    WHEN g.lex = false THEN 2
                                    ELSE 1
                                END))) AS glossed_morph,
                            json_agg(g.gloss_id) AS gl_ids,
                            u2m.place
                           FROM units u
                             JOIN langs l USING (lang_id)
                             JOIN units2morphs u2m USING (unit_id)
                             JOIN morphs m USING (lang_id, morph_id)
                             JOIN morph2glosses m2g USING (morph_id)
                             JOIN glosses g USING (gloss_id)
                          GROUP BY l.lang, u.unit, u2m.place, u.unit_id, m.morph_id, m.morph
                          ORDER BY u.unit, u2m.place) s
                  GROUP BY s.lang, s.unit, s.unit_id) t) t2;



-- DROP FUNCTION public.sort_gloss_string(varchar);

CREATE OR REPLACE FUNCTION public.sort_gloss_string(gl_string character varying)
 RETURNS character varying
 LANGUAGE sql
AS $function$
	with splitted as (
	select unnest(string_to_array(gl_string, '.')) spl),
	
	gl_detected as (
	select spl, case when spl=UPPER(spl) then 1 else 0 end gram
	from splitted
	),
	
	sorted_spl as (
		select spl from gl_detected order by (gram, spl)
	)
	
	select string_agg(spl, '.') from sorted_spl
$function$
;