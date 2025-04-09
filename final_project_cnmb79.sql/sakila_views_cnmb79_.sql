--1
CREATE VIEW monthlyRentalSales AS
SELECT YEAR(payment_date) AS year, MONTHNAME(payment_date) AS month, MONTH(payment_date) AS month_num, SUM(amount) AS TotalPayments
FROM payment
GROUP BY YEAR(payment_date), MONTHNAME(payment_date), MONTH(payment_date)
ORDER BY YEAR(payment_date), MONTH(payment_date);

--2
CREATE VIEW categoryTotals AS
SELECT YEAR(p.payment_date) AS year, c.name AS name, SUM(p.amount) AS TotalPayments
FROM payment p
JOIN rental r ON p.rental_id= r.rental_id
JOIN inventory i ON r.inventory_id= i.inventory_id
JOIN film_category f ON i.film_id= f.film_id
JOIN category c ON f.category_id= c.category_id
GROUP BY year, name
ORDER BY year ASC, name DESC;

--3
CREATE VIEW storeCitySales AS
SELECT c.city AS city, YEAR(p.payment_date) AS year, SUM(p.amount) AS TotalPayments
FROM payment p
JOIN rental r ON p.rental_id= r.rental_id
JOIN inventory i ON r.inventory_id= i.inventory_id
JOIN store s ON i.store_id= s.store_id
JOIN address a ON s.address_id=a.address_id
JOIN city c ON a.city_id=c.city_id
GROUP BY city, year
ORDER BY year DESC, city;

--4
CREATE VIEW customerRentalSales AS
SELECT YEAR(p.payment_date) AS year, CONCAT(c.first_name, " " ,c.last_name) AS name, SUM(p.amount) AS TotalPayments
FROM payment p
JOIN customer c ON c.customer_id= p.customer_id
GROUP BY year, name
ORDER BY year, TotalPayments DESC;

--5
CREATE VIEW customerMovieRentals AS
SELECT YEAR(p.payment_date) AS year, CONCAT(c.first_name, " " ,c.last_name) AS name, COUNT(r.rental_id) AS NumRentals
FROM payment p
JOIN rental r ON p.rental_id=r.rental_id
JOIN customer c ON c.customer_id= r.customer_id
GROUP BY year, name
ORDER BY year, NumRentals DESC;

--6
CREATE VIEW moviesPerCategory AS
SELECT c.name AS name, COUNT(f.film_id) AS NumMovies
FROM category c
JOIN film_category fc ON c.category_id=fc.category_id
JOIN film f ON fc.film_id=f.film_id
GROUP BY c.category_id
ORDER BY NumMovies DESC;

--7
CREATE VIEW moviesPerCategoryInStock AS
SELECT c.name AS name, COUNT(i.inventory_id) AS NumMovies
FROM category c
JOIN film_category fc ON c.category_id=fc.category_id
JOIN film f ON fc.film_id=f.film_id
JOIN inventory i ON f.film_id=i.film_id
WHERE i.inventory_id NOT IN (SELECT inventory_id FROM rental
WHERE return_date IS NULL)
GROUP BY c.category_id
ORDER BY NumMovies DESC;