CREATE TABLE IF NOT EXISTS crime_records (
    district_id INTEGER,
    district_name VARCHAR(255),
    crime_type VARCHAR(255),
    nearest_police_patrol FLOAT,
    population INTEGER,
    governor VARCHAR(255),
    day_of_week VARCHAR(20),
    date DATE,
    time TIME
);
