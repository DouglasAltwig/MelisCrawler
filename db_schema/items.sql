-- Table: public.items

-- DROP TABLE IF EXISTS public.items;

CREATE TABLE IF NOT EXISTS public.items
(
    site_id character(3) COLLATE pg_catalog."default" NOT NULL,
    item_id bigint NOT NULL,
    last_run date NOT NULL,
    category_id bigint,
    item_json json
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.items
    OWNER to postgres;