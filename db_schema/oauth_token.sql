-- Table: public.oauth_token

-- DROP TABLE IF EXISTS public.oauth_token;

CREATE SEQUENCE IF NOT EXISTS oauth_token_id_seq;

CREATE TABLE IF NOT EXISTS public.oauth_token
(
    id bigint NOT NULL DEFAULT nextval('oauth_token_id_seq'::regclass),
    access_token text COLLATE pg_catalog."default" NOT NULL,
    token_type text COLLATE pg_catalog."default" NOT NULL,
    expires_in integer NOT NULL,
    scope text[] COLLATE pg_catalog."default" NOT NULL,
    user_id bigint NOT NULL,
    refresh_token text COLLATE pg_catalog."default" NOT NULL,
    expires_at double precision NOT NULL,
    CONSTRAINT oauth_token_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.oauth_token
    OWNER to postgres;
-- Index: idx_oauth_token_access

-- DROP INDEX IF EXISTS public.idx_oauth_token_access;

CREATE INDEX IF NOT EXISTS idx_oauth_token_access
    ON public.oauth_token USING btree
    (access_token COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx_oauth_token_expires_at

-- DROP INDEX IF EXISTS public.idx_oauth_token_expires_at;

CREATE INDEX IF NOT EXISTS idx_oauth_token_expires_at
    ON public.oauth_token USING btree
    (expires_at ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx_oauth_token_refresh

-- DROP INDEX IF EXISTS public.idx_oauth_token_refresh;

CREATE INDEX IF NOT EXISTS idx_oauth_token_refresh
    ON public.oauth_token USING btree
    (refresh_token COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;