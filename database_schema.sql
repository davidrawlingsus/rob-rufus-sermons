-- Rob Rufus Sermon Directory - PostgreSQL Schema
-- This file shows the complete database schema for the sermon directory

-- Create the sermons table
CREATE TABLE IF NOT EXISTS sermons (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL UNIQUE,
    title VARCHAR(500) NOT NULL,
    date DATE NOT NULL,
    year INTEGER NOT NULL,
    themes JSONB NOT NULL,  -- PostgreSQL JSONB for better performance
    url VARCHAR(500) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_sermons_date ON sermons(date DESC);
CREATE INDEX IF NOT EXISTS idx_sermons_year ON sermons(year);
CREATE INDEX IF NOT EXISTS idx_sermons_title ON sermons USING gin(to_tsvector('english', title));
CREATE INDEX IF NOT EXISTS idx_sermons_themes ON sermons USING gin(themes);
CREATE INDEX IF NOT EXISTS idx_sermons_filename ON sermons(filename);

-- Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at
CREATE TRIGGER update_sermons_updated_at 
    BEFORE UPDATE ON sermons 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Sample data structure for themes JSONB field:
-- ["Grace & Gospel", "Anointing & Power", "Holy Spirit"]

-- Useful queries for the application:
-- 1. Search by theme: SELECT * FROM sermons WHERE themes ? 'Grace & Gospel';
-- 2. Search by multiple themes: SELECT * FROM sermons WHERE themes ?| array['Grace & Gospel', 'Holy Spirit'];
-- 3. Full-text search: SELECT * FROM sermons WHERE to_tsvector('english', title) @@ plainto_tsquery('english', 'grace');
-- 4. Date range: SELECT * FROM sermons WHERE date BETWEEN '2020-01-01' AND '2024-12-31';
