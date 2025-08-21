CREATE TABLE IF NOT EXISTS players(
    session_id VARCHAR(255) NOT NULL,
    game_state JSON NOT NULL
);

CREATE TABLE IF NOT EXISTS sesion(
    id VARCHAR(255) NOT NULL,
    session_guid VARCHAR(255) NOT NULL
);