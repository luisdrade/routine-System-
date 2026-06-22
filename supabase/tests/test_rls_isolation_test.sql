BEGIN;
SELECT plan(4);

-- Create mock users
INSERT INTO auth.users (id) VALUES 
('00000000-0000-0000-0000-000000000001'),
('00000000-0000-0000-0000-000000000002');

INSERT INTO public.users (id, full_name) VALUES 
('00000000-0000-0000-0000-000000000001', 'User 1'),
('00000000-0000-0000-0000-000000000002', 'User 2');

INSERT INTO public.workouts (id, user_id, name) VALUES 
('11111111-1111-1111-1111-111111111111', '00000000-0000-0000-0000-000000000001', 'Workout 1'),
('22222222-2222-2222-2222-222222222222', '00000000-0000-0000-0000-000000000002', 'Workout 2');

-- Switch to User 1
SET request.jwt.claims TO '{"sub": "00000000-0000-0000-0000-000000000001", "role": "authenticated"}';
SET ROLE authenticated;

SELECT results_eq(
    'SELECT name FROM public.workouts',
    $$VALUES ('Workout 1')$$,
    'User 1 should only see Workout 1'
);

-- Try inserting a workout for User 2 as User 1
SELECT throws_ok(
    $$INSERT INTO public.workouts (user_id, name) VALUES ('00000000-0000-0000-0000-000000000002', 'Hacked Workout')$$,
    'new row violates row-level security policy for table "workouts"',
    'User 1 cannot insert workout for User 2'
);

-- Switch to User 2
SET request.jwt.claims TO '{"sub": "00000000-0000-0000-0000-000000000002", "role": "authenticated"}';
SET ROLE authenticated;

SELECT results_eq(
    'SELECT name FROM public.workouts',
    $$VALUES ('Workout 2')$$,
    'User 2 should only see Workout 2'
);

-- Switch to anon role
SET request.jwt.claims TO '{"role": "anon"}';
SET ROLE anon;

SELECT is_empty(
    'SELECT * FROM public.workouts',
    'Anonymous user should not see any workouts'
);

SELECT * FROM finish();
ROLLBACK;
