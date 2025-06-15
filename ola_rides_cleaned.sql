USE ola_db;

-- Query 1: All successful bookings
SELECT * FROM ola_rides_cleaned WHERE booking_status = 'Success';

-- Query 2: Average ride distance per vehicle type
SELECT vehicle_type, AVG(ride_distance) AS avg_distance_km FROM ola_rides_cleaned
GROUP BY vehicle_type;

-- Query 3: Cancelled rides by customers
SELECT * FROM ola_rides_cleaned WHERE booking_status = 'Canceled by Customer';

-- Query 4: Top 5 customers by ride count
SELECT customer_id, COUNT(*) AS ride_count FROM ola_rides_cleaned GROUP BY customer_id
ORDER BY ride_count DESC LIMIT 5;

-- The dataset does not include detailed cancel reasons like 'personal' or 'car issues'.
-- All cancellations by drivers are labeled as 'No' under incomplete_rides.
-- Hence, returning all cancellations by drivers.
SELECT * FROM ola_rides_cleaned WHERE booking_status = 'Canceled by Driver';

-- Query 6: Max & Min driver ratings for Prime Sedan
SELECT MAX(driver_ratings) AS max_rating, MIN(driver_ratings) AS min_rating FROM ola_rides_cleaned
WHERE vehicle_type = 'Prime Sedan';

-- Query 7: Rides paid via UPI
SELECT * FROM ola_rides_cleaned WHERE payment_method = 'UPI';

-- Query 8: Average customer rating per vehicle type
SELECT vehicle_type, AVG(customer_rating) AS avg_customer_rating FROM ola_rides_cleaned
GROUP BY vehicle_type;

-- Query 9: Total value of completed bookings
SELECT SUM(booking_value) AS total_revenue FROM ola_rides_cleaned WHERE booking_status = 'Success';

-- Query 10: All incomplete rides with reason
SELECT booking_id, booking_status, incomplete_rides
FROM ola_rides_cleaned
WHERE booking_status != 'Success';


