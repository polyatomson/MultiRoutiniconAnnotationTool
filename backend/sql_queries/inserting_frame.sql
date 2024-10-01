with my_data(situation_structure, pragmatics, usage_conditions, sit_tags, situations) as 
(values (%s, %s, %s, %s, %s)
),

unfolded_conditions as (
	select unfolded.uc ->> 'condition' as "condition", unfolded.uc ->> 'category' as category 
	from (
		select jsonb_array_elements(m.usage_conditions::jsonb) uc 
		from my_data m) unfolded
	),
cond_ids as (
insert into conditions(category, "condition") 
select unfolded_conditions.category, unfolded_conditions."condition" from unfolded_conditions
on conflict("condition") do update set category=excluded.category
returning condition_id),

pragm_ids as (
	insert into pragmatics(pragmatics) select jsonb_array_elements_text(m.pragmatics::jsonb) from my_data m
	on conflict("pragmatics") do update  set pragmatics=excluded.pragmatics
	returning  pragmatics_id
),

sit_tag_ids as (
	insert into situation_tags(situation_tag) select jsonb_array_elements_text(m.sit_tags::jsonb) from my_data m
	on conflict("situation_tag") do update  set situation_tag=excluded.situation_tag
	returning  st_id
),

events_unfolded as (
	select sit_unf.sit ->> 'stage' stage, sit_unf.sit ->> 'event_type' "event" from 
	(select jsonb_array_elements(m.situations::jsonb) as sit from my_data m) sit_unf 
),

events_ids as (
	insert into events("event") select eunf."event" from events_unfolded as eunf
	on conflict("event") do update set "event"=excluded."event"
	returning event_id, "event"
),

events_w_types as (
	select events_ids.event_id, events_unfolded.stage
	from events_unfolded join events_ids on events_ids."event"=events_unfolded."event"
),

frame_unique_code(code) as (
	select 'c' || t.c || 'e' || t.e || 's' || t.s || 'p' || t.p from
		(select 
			my_data.situation_structure,
			string_agg(distinct cond_ids.condition_id::text, '|') c, 
			string_agg(distinct events_ids.event_id::text, '|') e, 
			string_agg(distinct sit_tag_ids.st_id::text, '|') s, 
			string_agg(distinct pragm_ids.pragmatics_id::text, '|') p 
			from 
			my_data, 
			(select * from cond_ids order by condition_id) cond_ids, 
			(select * from events_ids order by event_id) events_ids, 
			(select * from sit_tag_ids order by st_id) sit_tag_ids, 
			(select * from pragm_ids order by pragmatics_id) pragm_ids
			group by my_data.situation_structure
			) t
),

filled_frame as (
	insert into frames(situation_structure, unique_code) 
	select m.situation_structure, unic.code from my_data m, frame_unique_code unic
	returning frame_id
),

filled_f2e as (
	insert into frames2events(frame_id, event_id, stage)
	select * from filled_frame, events_w_types
	on conflict(frame_id, event_id, stage) do nothing
),


filled_f2c as (
	insert into frames2conditions(frame_id, condition_id)
	select * from filled_frame, cond_ids
	on conflict(frame_id, condition_id) do nothing
),

filled_f2p as (
	insert into frames2pragmatics(frame_id, pragmatics_id)
	select * from filled_frame, pragm_ids
	on conflict(frame_id, pragmatics_id) do nothing 
),

filled_f2st as (
insert into frames2st(frame_id, st_id)
select * from filled_frame, sit_tag_ids
on conflict(frame_id, st_id) do nothing)

select frame_id from filled_frame;