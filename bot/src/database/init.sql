CREATE TABLE IF NOT EXISTS sessions_user (
    user_id INT NOT NULL,
    session_guid UUID NOT NULL
    PRIMARY KEY (user_id, session_guid)
);