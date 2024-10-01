with r_examples(r_id) as (select jsonb_array_elements((%s::jsonb))
),

f (f_id) as (values(%s)),

r2f as (select * from r_examples cross join f)

insert into routines2frames (routine_id, frame_id) select r_id::integer, f_id from r2f
on conflict (routine_id, frame_id) do nothing;