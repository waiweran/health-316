\COPY location(uid, name, type, population, avg_income, gdp) FROM data/location.csv WITH DELIMITER ',' NULL '' CSV
\COPY in_location(uid, enclosing_id) FROM data/in_location.csv WITH DELIMITER ',' NULL '' CSV
