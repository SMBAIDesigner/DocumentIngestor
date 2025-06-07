-- Enable the pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create the documents table
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    original_filename VARCHAR(255) NOT NULL,
    summary_text TEXT,
    full_content TEXT,
    summary_vector VECTOR(384), -- Corresponds to paraphrase-multilingual-MiniLM-L12-v2
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Create an HNSW index for efficient similarity search.
-- HNSW is generally a good choice for high-dimensional, high-recall searching.
-- The ef_construction and m parameters can be tuned for performance vs. accuracy trade-offs.
CREATE INDEX IF NOT EXISTS documents_summary_vector_idx ON documents USING hnsw (summary_vector vector_l2_ops);

-- Example of an IVFFlat index, which can be faster for very large datasets
-- if a small recall trade-off is acceptable.
-- CREATE INDEX ON documents USING ivfflat (summary_vector vector_l2_ops) WITH (lists = 100);

COMMENT ON TABLE documents IS 'Stores processed PDF documents, their content, and vector embeddings.';
COMMENT ON COLUMN documents.id IS 'Unique identifier for each document';
COMMENT ON COLUMN documents.original_filename IS 'The name of the source PDF file';
COMMENT ON COLUMN documents.summary_text IS 'AI-generated summary (max 200 chars)';
COMMENT ON COLUMN documents.full_content IS 'Full extracted text content in Markdown format';
COMMENT ON COLUMN documents.summary_vector IS 'Vector embedding of the summary_text';
COMMENT ON COLUMN documents.created_at IS 'Timestamp of when the record was created'; 