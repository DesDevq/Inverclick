ALTER TABLE public.users_login
ADD COLUMN identity_provider varchar DEFAULT 'local' NOT NULL;

ALTER TABLE public.users_login
ADD COLUMN external_id varchar;