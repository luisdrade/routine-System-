-- Create tables

CREATE TABLE public.users (
  id UUID REFERENCES auth.users(id) PRIMARY KEY,
  full_name TEXT,
  created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
  updated_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

CREATE TABLE public.exercises (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  target_muscle_group TEXT,
  user_id UUID REFERENCES public.users(id), -- null means global exercise
  created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

CREATE TABLE public.workouts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  started_at TIMESTAMPTZ DEFAULT now() NOT NULL,
  completed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

CREATE TABLE public.sets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workout_id UUID NOT NULL REFERENCES public.workouts(id) ON DELETE CASCADE,
  exercise_id UUID NOT NULL REFERENCES public.exercises(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
  reps INT NOT NULL,
  weight_kg NUMERIC(6,2) NOT NULL,
  rpe NUMERIC(3,1),
  completed BOOLEAN DEFAULT false NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

CREATE TABLE public.physique_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
  weight_kg NUMERIC(5,2),
  body_fat_percentage NUMERIC(4,2),
  photo_url TEXT,
  vision_analysis JSONB,
  logged_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

CREATE TABLE public.diet_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
  calories INT,
  protein_g NUMERIC(5,1),
  carbs_g NUMERIC(5,1),
  fat_g NUMERIC(5,1),
  logged_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

CREATE TABLE public.progression_rules (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
  exercise_id UUID NOT NULL REFERENCES public.exercises(id) ON DELETE CASCADE,
  target_rpe_min NUMERIC(3,1) DEFAULT 7.0,
  target_rpe_max NUMERIC(3,1) DEFAULT 8.0,
  increment_percentage NUMERIC(4,2) DEFAULT 2.5,
  decrement_percentage NUMERIC(4,2) DEFAULT 5.0,
  created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
  UNIQUE(user_id, exercise_id)
);

-- Enable RLS
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.exercises ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.workouts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.sets ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.physique_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.diet_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.progression_rules ENABLE ROW LEVEL SECURITY;

-- RLS Policies (MVP Pessoal: Autenticado tem acesso total)

-- Users
CREATE POLICY "Full access to authenticated users" ON public.users FOR ALL TO authenticated USING (true) WITH CHECK (true);

-- Exercises
CREATE POLICY "Full access to authenticated users" ON public.exercises FOR ALL TO authenticated USING (true) WITH CHECK (true);

-- Workouts
CREATE POLICY "Full access to authenticated users" ON public.workouts FOR ALL TO authenticated USING (true) WITH CHECK (true);

-- Sets
CREATE POLICY "Full access to authenticated users" ON public.sets FOR ALL TO authenticated USING (true) WITH CHECK (true);

-- Physique Logs
CREATE POLICY "Full access to authenticated users" ON public.physique_logs FOR ALL TO authenticated USING (true) WITH CHECK (true);

-- Diet Logs
CREATE POLICY "Full access to authenticated users" ON public.diet_logs FOR ALL TO authenticated USING (true) WITH CHECK (true);

-- Progression Rules
CREATE POLICY "Full access to authenticated users" ON public.progression_rules FOR ALL TO authenticated USING (true) WITH CHECK (true);

-- Storage bucket for physique photos (non-public, strictly signed URLs)
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES ('physique_photos', 'physique_photos', false, 10485760, '{"image/jpeg","image/png","image/webp"}')
ON CONFLICT (id) DO NOTHING;

-- RLS for Storage Objects (only bucket_id = physique_photos)
CREATE POLICY "Full access to authenticated users" ON storage.objects FOR ALL TO authenticated USING (bucket_id = 'physique_photos') WITH CHECK (bucket_id = 'physique_photos');
