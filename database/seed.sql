-- ============================================
-- Seed data for Study Room Reservation System
-- ============================================

-- Students
INSERT INTO student (name, email) VALUES
    ('Amine EL', 'amine@example.com'),
    ('Sara Ben', 'sara@example.com'),
    ('Youssef Ala', 'youssef@example.com'),
    ('Nora Had', 'nora@example.com');


-- Study rooms
INSERT INTO room (room_number, capacity) VALUES
    ('R101', 4),
    ('R102', 6),
    ('R201', 8),
    ('R202', 12);


-- Equipment
INSERT INTO equipment (name) VALUES
    ('Projector'),
    ('Whiteboard'),
    ('Monitor'),
    ('Video Conference');


-- Room equipment
INSERT INTO room_equipment (room_id, equipment_id)
SELECT r.room_id, e.equipment_id
FROM room r, equipment e
WHERE r.room_number = 'R101'
  AND e.name IN ('Whiteboard', 'Monitor');

INSERT INTO room_equipment (room_id, equipment_id)
SELECT r.room_id, e.equipment_id
FROM room r, equipment e
WHERE r.room_number = 'R102'
  AND e.name IN ('Projector', 'Whiteboard');

INSERT INTO room_equipment (room_id, equipment_id)
SELECT r.room_id, e.equipment_id
FROM room r, equipment e
WHERE r.room_number = 'R201'
  AND e.name IN ('Projector', 'Whiteboard', 'Monitor');

INSERT INTO room_equipment (room_id, equipment_id)
SELECT r.room_id, e.equipment_id
FROM room r, equipment e
WHERE r.room_number = 'R202'
  AND e.name IN ('Projector', 'Whiteboard', 'Monitor', 'Video Conference');


-- Reservations
INSERT INTO reservation
    (date, start_time, end_time, student_id, room_id)
SELECT
    DATE '2026-08-20',
    TIME '10:00',
    TIME '12:00',
    s.student_id,
    r.room_id
FROM student s, room r
WHERE s.email = 'amine@example.com'
  AND r.room_number = 'R101';


INSERT INTO reservation
    (date, start_time, end_time, student_id, room_id)
SELECT
    DATE '2026-08-20',
    TIME '14:00',
    TIME '16:00',
    s.student_id,
    r.room_id
FROM student s, room r
WHERE s.email = 'sara@example.com'
  AND r.room_number = 'R102';


INSERT INTO reservation
    (date, start_time, end_time, student_id, room_id)
SELECT
    DATE '2026-08-21',
    TIME '09:00',
    TIME '11:00',
    s.student_id,
    r.room_id
FROM student s, room r
WHERE s.email = 'youssef@example.com'
  AND r.room_number = 'R201';


INSERT INTO reservation
    (date, start_time, end_time, student_id, room_id)
SELECT
    DATE '2026-08-22',
    TIME '13:00',
    TIME '15:00',
    s.student_id,
    r.room_id
FROM student s, room r
WHERE s.email = 'nora@example.com'
  AND r.room_number = 'R202';