-- Table: public.base_categories

-- DROP TABLE IF EXISTS public.base_categories;

CREATE TABLE IF NOT EXISTS public.base_categories
(
    site_id character(3) COLLATE pg_catalog."default" NOT NULL,
    category_id bigint NOT NULL,
    last_run date NOT NULL,
    category_json json
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.base_categories
    OWNER to postgres;