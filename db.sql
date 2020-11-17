CREATE TABLE public.project
(
    id uuid NOT NULL,
    created_on timestamp with time zone NOT NULL,
    updated_on timestamp with time zone NOT NULL,
    name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    notes text COLLATE pg_catalog."default" NOT NULL,
    status smallint NOT NULL,
    updated_by_id uuid,
    data_policy_beltfish smallint NOT NULL,
    data_policy_benthiclit smallint NOT NULL,
    data_policy_benthicpit smallint NOT NULL,
    data_policy_habitatcomplexity smallint NOT NULL,
    data_policy_bleachingqc smallint NOT NULL,
    created_by_id uuid,
    CONSTRAINT project_pkey PRIMARY KEY (id),
    CONSTRAINT project_name_0c79925e_uniq UNIQUE (name)
);

CREATE INDEX project_created_by_id_6cc13408
    ON public.project USING btree
    (created_by_id ASC NULLS LAST)
    TABLESPACE pg_default;


CREATE TABLE public.site
(
    id uuid NOT NULL,
    created_on timestamp with time zone NOT NULL,
    updated_on timestamp with time zone NOT NULL,
    data jsonb,
    name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    location geometry(Point,4326) NOT NULL,
    notes text COLLATE pg_catalog."default" NOT NULL,
    country_id uuid NOT NULL,
    exposure_id uuid NOT NULL,
    project_id uuid NOT NULL,
    reef_type_id uuid NOT NULL,
    reef_zone_id uuid NOT NULL,
    updated_by_id uuid,
    predecessor_id uuid,
    validations jsonb,
    created_by_id uuid,
    CONSTRAINT site_pkey PRIMARY KEY (id),
    CONSTRAINT site_project_id_c3f7cde0_fk_project_id FOREIGN KEY (project_id)
        REFERENCES public.project (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        DEFERRABLE INITIALLY DEFERRED
);

CREATE INDEX site_predecessor_id_bb824e35
    ON public.site USING btree
    (predecessor_id ASC NULLS LAST)
    TABLESPACE pg_default;