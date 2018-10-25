\COPY DataPoint(condition_id, location_id, prevalence, incidence, mortality, year, min_age, max_age, gender, race/ethnicity) FROM 'data/datapoint.dat' WITH DELIMITER ',' NULL '' CSV
\COPY Condition(condition_id) FROM 'data/condition.dat' WITH DELIMITER ',' NULL '' CSV
\COPY ConditionName(name, condition_id) FROM 'data/condition_name.dat' WITH DELIMITER ',' NULL '' CSV
\COPY inLocation(uid, enclosing) FROM 'data/in_location.dat' WITH DELIMITER ',' NULL '' CSV
\COPY Location(uid,name,type,population,avg_income,gdp) FROM 'data/location.dat' WITH DELIMITER ',' NULL '' CSV
