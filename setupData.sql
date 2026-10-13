INSERT INTO building (building_id, name, abbreviation) VALUES
(1, 'Harris Fine Arts Center', 'HFAC'),
(2, 'Wilkinson Student Center', 'WSC'),
(3, 'Harold B. Lee Library', 'HBLL'),
(4, 'Joseph Smith Building', 'JSB'),
(5, 'Brimhall Building', 'BRMB');

INSERT INTO room (room_id, building_id, room_number, room_type) VALUES
(1, 1, 'C-550', 'concert hall'),
(2, 1, 'C-301', 'practice room'),
(3, 1, 'C-302', 'practice room'),
(4, 1, 'C-303', 'practice room'),
(5, 1, 'D-410', 'studio'),
(6, 2, 'Lobby', 'lounge'),
(7, 2, '3rd Floor', 'lounge'),
(8, 3, '2nd Floor', 'lounge'),
(9, 4, 'B-101', 'classroom'),
(10, 4, 'B-102', 'classroom'),
(11, 5, '120', 'practice room'),
(12, 5, '121', 'practice room');

INSERT INTO piano (piano_id, room_id, brand, model, piano_type, serial_number, year_made, status) VALUES
(1, 1, 'Steinway & Sons', 'Model D', 'grand', 'ST-100234', 2015, 'active'),
(2, 2, 'Yamaha', 'U1', 'upright', 'YM-554201', 2008, 'active'),
(3, 3, 'Yamaha', 'U1', 'upright', 'YM-554377', 2008, 'needs repair'),
(4, 4, 'Kawai', 'K-300', 'upright', 'KW-882910', 2012, 'active'),
(5, 5, 'Steinway & Sons', 'Model B', 'grand', 'ST-098812', 1998, 'active'),
(6, 6, 'Baldwin', 'Hamilton', 'upright', 'BW-310045', 1985, 'needs repair'),
(7, 7, 'Yamaha', 'P-125', 'digital', 'YM-D77120', 2020, 'active'),
(8, 8, 'Kawai', 'GL-10', 'baby grand', 'KW-770012', 2016, 'active'),
(9, 9, 'Young Chang', 'G-157', 'baby grand', 'YC-440981', 2001, 'active'),
(10, 10, 'Yamaha', 'U3', 'upright', 'YM-300998', 1995, 'active'),
(11, 11, 'Kawai', 'K-300', 'upright', 'KW-882955', 2012, 'active'),
(12, 12, 'Baldwin', 'Acrosonic', 'upright', 'BW-210077', 1978, 'retired'),
(13, NULL, 'Steinway & Sons', 'Model M', 'baby grand', 'ST-071122', 1989, 'retired'),
(14, 2, 'Roland', 'FP-30X', 'digital', 'RL-D55671', 2022, 'active');

INSERT INTO technician (technician_id, name, phone, is_certified) VALUES
(1, 'Marcus Webb', '801-555-0142', 1),
(2, 'Elena Petrova', '801-555-0177', 1),
(3, 'Tom Alvarez', NULL, 0);

INSERT INTO tuning (tuning_id, piano_id, technician_id, tuning_date, notes) VALUES
(1, 1, 1, '2025-08-15', 'Pre-semester concert tuning'),
(2, 1, 1, '2026-01-10', 'Winter tuning'),
(3, 1, 1, '2026-08-20', 'Pre-semester concert tuning'),
(4, 2, 2, '2026-01-12', NULL),
(5, 2, 2, '2026-08-22', NULL),
(6, 3, 2, '2026-01-12', 'Sticky keys noted'),
(7, 4, 2, '2026-08-22', NULL),
(8, 5, 1, '2026-03-03', 'Pitch raise needed'),
(9, 5, 1, '2026-08-20', NULL),
(10, 6, 3, '2024-05-14', 'Very out of tune'),
(11, 8, 1, '2026-06-18', NULL),
(12, 9, 3, '2025-11-02', NULL),
(13, 10, 2, '2026-02-20', NULL),
(14, 11, 2, '2026-08-22', NULL),
(15, 12, 3, '2023-09-09', 'Last service before retirement');

INSERT INTO student (student_id, name, email, major) VALUES
(1, 'Anna Larsen', 'anna.larsen@example.edu', 'Piano Performance'),
(2, 'Ben Okafor', 'ben.okafor@example.edu', 'Music Education'),
(3, 'Chloe Nguyen', NULL, 'Computer Science'),
(4, 'David Kim', 'david.kim@example.edu', 'Composition'),
(5, 'Emily Rivera', 'emily.rivera@example.edu', 'Nursing'),
(6, 'Frank Holt', 'frank.holt@example.edu', 'Piano Performance');

INSERT INTO repair_request (request_id, piano_id, student_id, reported_date, description, severity, status, resolved_date) VALUES
(1, 3, 1, '2026-09-02', 'Several keys sticking in the middle octave', 'medium', 'in progress', NULL),
(2, 3, 2, '2026-09-10', 'Sustain pedal does not release', 'high', 'open', NULL),
(3, 6, 3, '2026-08-25', 'Many notes out of tune and a broken key', 'high', 'open', NULL),
(4, 1, NULL, '2026-02-14', 'Squeaky pedal', 'low', 'resolved', '2026-02-20'),
(5, 5, 4, '2026-04-01', 'Buzzing on low A', 'medium', 'resolved', '2026-04-09'),
(6, 9, 6, '2026-09-20', 'Music stand is loose', 'low', 'open', NULL),
(7, 12, 5, '2025-12-01', 'Cracked soundboard', 'high', 'resolved', '2026-01-15'),
(8, 10, NULL, '2026-09-28', 'Middle C does not sound', 'medium', 'in progress', NULL);

INSERT INTO reservation (reservation_id, piano_id, student_id, start_time, end_time) VALUES
(1, 2, 1, '2026-10-05 09:00', '2026-10-05 11:00'),
(2, 2, 6, '2026-10-05 11:00', '2026-10-05 12:00'),
(3, 4, 1, '2026-10-06 14:00', '2026-10-06 16:00'),
(4, 4, 4, '2026-10-07 10:00', '2026-10-07 11:00'),
(5, 5, 1, '2026-10-08 13:00', '2026-10-08 15:00'),
(6, 5, 6, '2026-10-09 13:00', '2026-10-09 14:00'),
(7, 11, 2, '2026-10-06 08:00', '2026-10-06 09:00'),
(8, 3, 2, '2026-10-05 15:00', '2026-10-05 16:00'),
(9, 14, 3, '2026-10-07 18:00', '2026-10-07 19:00'),
(10, 2, 5, '2026-10-08 19:00', '2026-10-08 20:00'),
(11, 1, 1, '2026-10-10 16:00', '2026-10-10 18:00');
