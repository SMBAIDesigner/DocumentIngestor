CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS documents (
        id SERIAL PRIMARY KEY,
        filename TEXT NOT NULL UNIQUE,
        summary_embedding vector({VECTOR_DIMENSION}),
        summary_content TEXT,
        original_content TEXT
    );

CREATE INDEX IF NOT EXISTS documents_summary_embedding_idx 
ON documents 
USING hnsw (summary_embedding vector_l2_ops);