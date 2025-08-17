
-- 15 SQL questions used by the app

-- 1. Providers & Receivers per City
SELECT city, 
       (SELECT COUNT(*) FROM Providers pr WHERE pr.city = p.city) AS providers_count,
       (SELECT COUNT(*) FROM Receivers r WHERE r.city = p.city) AS receivers_count
FROM Providers p
WHERE p.city IS NOT NULL AND p.city<>''
GROUP BY city
ORDER BY city;

-- 2. Quantity by Provider Type
SELECT provider_type, COALESCE(SUM(quantity),0) AS total_quantity
FROM Food_Listings
GROUP BY provider_type
ORDER BY total_quantity DESC;

-- 3. Provider Contacts by City
SELECT name, provider_type, city, contact FROM Providers WHERE city = 'Delhi' ORDER BY name;

-- 4. Top Receivers by Claimed Quantity
SELECT r.receiver_id, r.name, r.city, COALESCE(SUM(fl.quantity),0) AS total_claimed
FROM Claims c
JOIN Receivers r ON r.receiver_id = c.receiver_id
JOIN Food_Listings fl ON fl.food_id = c.food_id
GROUP BY r.receiver_id, r.name, r.city
ORDER BY total_claimed DESC;

-- 5. Total Available (not expired)
SELECT COALESCE(SUM(quantity),0) AS total_available
FROM Food_Listings
WHERE expiry_date >= CURDATE();

-- 6. Listings by City
SELECT location AS city, COUNT(*) AS listings_count
FROM Food_Listings
GROUP BY location
ORDER BY listings_count DESC;

-- 7. Most Common Food Types
SELECT food_type, COUNT(*) AS listings
FROM Food_Listings
GROUP BY food_type
ORDER BY listings DESC;

-- 8. Claims per Food Item
SELECT fl.food_id, fl.food_name, COUNT(c.claim_id) AS claims_count
FROM Food_Listings fl
LEFT JOIN Claims c ON c.food_id = fl.food_id
GROUP BY fl.food_id, fl.food_name
ORDER BY claims_count DESC;

-- 9. Providers by Successful Claims
SELECT p.provider_id, p.name, COUNT(*) AS successful_claims
FROM Claims c
JOIN Food_Listings fl ON fl.food_id = c.food_id
JOIN Providers p ON p.provider_id = fl.provider_id
WHERE c.status='Completed'
GROUP BY p.provider_id, p.name
ORDER BY successful_claims DESC;

-- 10. Claims Status Distribution
SELECT status,
       COUNT(*) AS count_status,
       ROUND(COUNT(*)*100.0 / (SELECT COUNT(*) FROM Claims), 2) AS pct
FROM Claims
GROUP BY status
ORDER BY count_status DESC;

-- 11. Avg Quantity Claimed per Receiver
SELECT r.receiver_id, r.name, ROUND(AVG(fl.quantity),2) AS avg_qty_claimed
FROM Claims c
JOIN Receivers r ON r.receiver_id = c.receiver_id
JOIN Food_Listings fl ON fl.food_id = c.food_id
GROUP BY r.receiver_id, r.name
ORDER BY avg_qty_claimed DESC;

-- 12. Most Claimed Meal Type
SELECT fl.meal_type, COUNT(*) AS claims_count
FROM Claims c
JOIN Food_Listings fl ON fl.food_id = c.food_id
GROUP BY fl.meal_type
ORDER BY claims_count DESC;

-- 13. Total Donated by Provider
SELECT p.provider_id, p.name, COALESCE(SUM(fl.quantity),0) AS total_donated
FROM Providers p
LEFT JOIN Food_Listings fl ON fl.provider_id = p.provider_id
GROUP BY p.provider_id, p.name
ORDER BY total_donated DESC;

-- 14. Wastage by City (expired qty)
SELECT fl.location AS city, COALESCE(SUM(fl.quantity),0) AS expired_qty
FROM Food_Listings fl
WHERE fl.expiry_date < CURDATE()
GROUP BY fl.location
ORDER BY expired_qty DESC;

-- 15. Listings Expiring within 7 days
SELECT fl.food_id, fl.food_name, fl.location, fl.quantity, fl.expiry_date, p.name AS provider
FROM Food_Listings fl
JOIN Providers p ON p.provider_id = fl.provider_id
WHERE fl.expiry_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)
ORDER BY fl.expiry_date;
