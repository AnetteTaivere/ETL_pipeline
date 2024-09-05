CREATE TABLE IF NOT EXISTS search_data (
        id SERIAL PRIMARY KEY,
        term VARCHAR(255) NOT NULL,
        incidence INT NOT NULL,
        site VARCHAR(50) NOT NULL,
        timestamp TIMESTAMPTZ NOT NULL
    );