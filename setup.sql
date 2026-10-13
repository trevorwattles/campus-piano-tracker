create table building (
    building_id integer primary key,
    name varchar(50) not null,
    abbreviation varchar(10) not null
);

create table room (
    room_id integer primary key,
    building_id integer not null,
    room_number varchar(10) not null,
    room_type varchar(20) not null, -- 'practice room', 'classroom', 'concert hall', 'lounge', 'studio'
    foreign key (building_id) references building (building_id)
);

create table piano (
    piano_id integer primary key,
    room_id integer, -- NULL means the piano is in storage / not placed in a room
    brand varchar(30) not null,
    model varchar(30),
    piano_type varchar(15) not null, -- 'upright', 'grand', 'baby grand', 'digital'
    serial_number varchar(20),
    year_made integer,
    status varchar(15) not null, -- 'active', 'needs repair', 'retired'
    foreign key (room_id) references room (room_id)
);

create table technician (
    technician_id integer primary key,
    name varchar(40) not null,
    phone varchar(15),
    is_certified tinyint not null -- 1 = Registered Piano Technician, 0 = not
);

create table tuning (
    tuning_id integer primary key,
    piano_id integer not null,
    technician_id integer not null,
    tuning_date date not null,
    notes varchar(100),
    foreign key (piano_id) references piano (piano_id),
    foreign key (technician_id) references technician (technician_id)
);

create table student (
    student_id integer primary key,
    name varchar(40) not null,
    email varchar(50),
    major varchar(40)
);

create table repair_request (
    request_id integer primary key,
    piano_id integer not null,
    student_id integer, -- NULL when reported by staff
    reported_date date not null,
    description varchar(100) not null,
    severity varchar(10) not null, -- 'low', 'medium', 'high'
    status varchar(12) not null, -- 'open', 'in progress', 'resolved'
    resolved_date date,
    foreign key (piano_id) references piano (piano_id),
    foreign key (student_id) references student (student_id)
);

create table reservation (
    reservation_id integer primary key,
    piano_id integer not null,
    student_id integer not null,
    start_time datetime not null,
    end_time datetime not null,
    foreign key (piano_id) references piano (piano_id),
    foreign key (student_id) references student (student_id)
);
