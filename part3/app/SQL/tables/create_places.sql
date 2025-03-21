CREATE TABLE IF NOT EXISTS places (
    id CHAR(36) NOT NULL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id CHAR(36) NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE,
);

-- if you put ON DELETE SET NULL, this will keep the place id and set it to null
-- and this way the place will remained even when the user dissapears