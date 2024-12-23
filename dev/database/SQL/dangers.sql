CREATE TABLE dangers (
    danger_id VARCHAR(255) PRIMARY KEY,
    camera_id VARCHAR(255) NOT NULL,
    coordinate_p1 INT NOT NULL,
    coordinate_p2 INT NOT NULL,
    coordinate_p3 INT NOT NULL,
    coordinate_p4 INT NOT NULL,
    CONSTRAINT fk_camera FOREIGN KEY (camera_id) REFERENCES cameras(camera_id)
);
