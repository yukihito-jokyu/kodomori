CREATE TABLE cameras (
    camera_id VARCHAR(255) PRIMARY KEY,
    nursery_school_id VARCHAR(255),
    is_setting_floor_area BOOLEAN NOT NULL,
    picture BOOLEAN NOT NULL,
    distance_p1_p2 INT NOT NULL,
    distance_p1_p3 INT NOT NULL,
    distance_p1_p4 INT NOT NULL,
    distance_p2_p3 INT NOT NULL,
    distance_p2_p4 INT NOT NULL,
    distance_p3_p4 INT NOT NULL,
    coordinate_p1 INT NOT NULL,
    coordinate_p2 INT NOT NULL,
    coordinate_p3 INT NOT NULL,
    coordinate_p4 INT NOT NULL,
    CONSTRAINT fk_nursery_school FOREIGN KEY (nursery_school_id) REFERENCES users(user_id)
);
