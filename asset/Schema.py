weather_records = """
CREATE TABLE weather_records (
    record_time DATETIME NOT NULL,
    station_id VARCHAR(50) NOT NULL,
    station_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    station_latitude DECIMAL(10, 8) NOT NULL,
    station_longitude DECIMAL(11, 8) NOT NULL,
    country_name VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    town_name VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    weather_description TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    data_write_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    PRIMARY KEY (station_id, record_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

"""