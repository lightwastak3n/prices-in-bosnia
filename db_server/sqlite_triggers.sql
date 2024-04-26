CREATE TRIGGER insert_new_land
AFTER INSERT ON land
BEGIN
    UPDATE scraping_stats SET land = land + 1 WHERE id = 0;
END;

CREATE TRIGGER insert_new_house
AFTER INSERT ON houses
BEGIN
    UPDATE scraping_stats SET houses = houses + 1
END;

CREATE TRIGGER insert_new_flats
AFTER INSERT ON flats
BEGIN
    UPDATE scraping_stats SET flats = flats + 1
END;

CREATE TRIGGER insert_new_car
AFTER INSERT ON cars
BEGIN
    UPDATE scraping_stats SET cars = cars + 1
END;