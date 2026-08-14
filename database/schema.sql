CREATE TABLE student (
    student_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(200) NOT NULL UNIQUE
);

CREATE TABLE room (
    room_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    room_number VARCHAR(20) NOT NULL UNIQUE,
    capacity INTEGER NOT NULL CHECK (capacity > 0)
);

CREATE TABLE equipment (
    equipment_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE reservation (
    reservation_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    student_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,

    CHECK (end_time > start_time),

    FOREIGN KEY (student_id)
        REFERENCES student (student_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    FOREIGN KEY (room_id)
        REFERENCES room (room_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE room_equipment (
    room_id INTEGER NOT NULL,
    equipment_id INTEGER NOT NULL,

    PRIMARY KEY (room_id, equipment_id),

    FOREIGN KEY (room_id)
        REFERENCES room (room_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (equipment_id)
        REFERENCES equipment (equipment_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);