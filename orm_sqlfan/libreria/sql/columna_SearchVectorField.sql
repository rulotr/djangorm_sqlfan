ALTER TABLE public.libreria_libro  drop COLUMN IF EXISTS dsc_corta_token;
ALTER TABLE public.libreria_libro 
ADD COLUMN dsc_corta_token tsvector
               GENERATED ALWAYS AS (to_tsvector('english', coalesce(titulo, '') || ' ' || coalesce(desc_corta, ''))) STORED;
