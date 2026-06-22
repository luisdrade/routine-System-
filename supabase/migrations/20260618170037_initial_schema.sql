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

-- RLS Policies

-- Users
CREATE POLICY "Users can view their own profile" ON public.users FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update their own profile" ON public.users FOR UPDATE USING (auth.uid() = id);
CREATE POLICY "Users can insert their own profile" ON public.users FOR INSERT WITH CHECK (auth.uid() = id);

-- Exercises
CREATE POLICY "Users can view global or own exercises" ON public.exercises FOR SELECT USING (user_id IS NULL OR user_id = auth.uid());
CREATE POLICY "Users can insert own exercises" ON public.exercises FOR INSERT WITH CHECK (user_id = auth.uid());
CREATE POLICY "Users can update own exercises" ON public.exercises FOR UPDATE USING (user_id = auth.uid());
CREATE POLICY "Users can delete own exercises" ON public.exercises FOR DELETE USING (user_id = auth.uid());

-- Workouts
CREATE POLICY "Users can view their own workouts" ON public.workouts FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert their own workouts" ON public.workouts FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update their own workouts" ON public.workouts FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete their own workouts" ON public.workouts FOR DELETE USING (auth.uid() = user_id);

-- Sets
CREATE POLICY "Users can view their own sets" ON public.sets FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert their own sets" ON public.sets FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update their own sets" ON public.sets FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete their own sets" ON public.sets FOR DELETE USING (auth.uid() = user_id);

-- Physique Logs
CREATE POLICY "Users can view their own physique logs" ON public.physique_logs FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert their own physique logs" ON public.physique_logs FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update their own physique logs" ON public.physique_logs FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete their own physique logs" ON public.physique_logs FOR DELETE USING (auth.uid() = user_id);

-- Diet Logs
CREATE POLICY "Users can view their own diet logs" ON public.diet_logs FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert their own diet logs" ON public.diet_logs FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update their own diet logs" ON public.diet_logs FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete their own diet logs" ON public.diet_logs FOR DELETE USING (auth.uid() = user_id);

-- Progression Rules
CREATE POLICY "Users can view their own progression rules" ON public.progression_rules FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert their own progression rules" ON public.progression_rules FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update their own progression rules" ON public.progression_rules FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete their own progression rules" ON public.progression_rules FOR DELETE USING (auth.uid() = user_id);

-- Storage bucket for physique photos (non-public, strictly signed URLs)
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES ('physique_photos', 'physique_photos', false, 10485760, '{"image/jpeg","image/png","image/webp"}')
ON CONFLICT (id) DO NOTHING;

-- RLS for Storage Objects (only bucket_id = physique_photos)
-- Note: owner column in storage.objects is populated automatically by Supabase with auth.uid() if authenticated.
CREATE POLICY "Users can upload their own photos" ON storage.objects FOR INSERT TO authenticated WITH CHECK (bucket_id = 'physique_photos' AND auth.uid() = owner);
CREATE POLICY "Users can view their own photos" ON storage.objects FOR SELECT TO authenticated USING (bucket_id = 'physique_photos' AND auth.uid() = owner);
CREATE POLICY "Users can update their own photos" ON storage.objects FOR UPDATE TO authenticated USING (bucket_id = 'physique_photos' AND auth.uid() = owner);
CREATE POLICY "Users can delete their own photos" ON storage.objects FOR DELETE TO authenticated USING (bucket_id = 'physique_photos' AND auth.uid() = owner);
