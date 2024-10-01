with my_data(usage_conditions) as 
(values ('[{"category":"time", "condition": "The conversation takes place in the morning"}, {"category":"place", "condition": "The speaker and the interlocutor slept in the same location"}]'::jsonb)
),

unfolded_conditions as (
	select unfolded.uc ->> 'condition' as "condition", unfolded.uc ->> 'category' as category 
	from (
		select jsonb_array_elements(m.usage_conditions) uc 
		from my_data m) unfolded
	),
cond_ids as (
insert into conditions(category, "condition") 
select unfolded_conditions.category, unfolded_conditions."condition" from unfolded_conditions
on conflict("condition") do update set category=excluded.category
returning condition_id),



select * from cond_ids;