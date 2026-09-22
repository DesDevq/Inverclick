ALTER TABLE public.users_login ADD COLUMN IF NOT EXISTS identity_provider varchar NOT NULL DEFAULT 'local';
ALTER TABLE public.users_login ADD COLUMN IF NOT EXISTS external_id varchar;