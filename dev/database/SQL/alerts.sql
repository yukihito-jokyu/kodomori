CREATE TABLE alerts (
    alert_id VARCHAR(255) PRIMARY KEY,
    nursery_school_id VARCHAR(255) NOT NULL,
    message VARCHAR(255) NOT NULL,
    is_read BOOLEAN NOT NULL,
    time TIMESTAMP NOT NULL,
    CONSTRAINT fk_nursery_school FOREIGN KEY (nursery_school_id) REFERENCES users(user_id)
);
