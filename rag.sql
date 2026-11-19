create extension if not exists vector with schema public;

create table if not exists public.rag_chunks (
    id          bigint generated always as identity primary key,
    source      text not null,
    title       text,
    page        integer,
    chunk_index integer not null,
    content     text not null,
    embedding   public.vector(1024) not null,
    metadata    jsonb not null default '{}'::jsonb,
    created_at  timestamptz not null default now(),
    constraint rag_chunks_source_chunk_unique unique (source, chunk_index)
);

create index if not exists rag_chunks_embeddings_hnsw
    on public.rag_chunks
    using hnsw (embedding public.vector_cosine_ops)
    with (m = 16, ef_construction = 64);

create index if not exists rag_chunks_source_idx
    on public.rag_chunks (source);

alter table public.rag_chunks enable row level security;

grant all on table public.rag_chunks to service_role;
grant all on sequence public.rag_chunks_id_seq to service_role;