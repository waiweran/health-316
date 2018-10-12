--Most common disease in location among males
SELECT Max(incidence)
FROM Datapoint
WHERE gender = 'Male'
GROUP BY location_id;

--GDP of locations with Asian people who have mortality greater than 0.1 for any disease
SELECT location.name, location.gdp
FROM location NATURAL JOIN Datapoint AS dp
WHERE dp.race_ethnicity = 'Asian' AND dp.mortality > 0.1
ORDER BY location.gdp DESC, location.name ASC;

--number of states who do not have data on HIV for black people in 2015

SELECT Count(*)
FROM
( SELECT DISTINCT location.name
FROM location 
WHERE type = 'state'

EXCEPT ALL

SELECT DISTINCT location.name
FROM location NATURAL JOIN datapoint AS dp NATURAL JOIN condition
WHERE dp.year = 2015 AND dp.race_ethnicity = 'black' AND conditionName = 'HIV'
);