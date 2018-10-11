CREATE TABLE location (
	uid INT UNSIGNED NOT NULL PRIMARY KEY,
	name VARCHAR(256) NOT NULL,
	type CHAR(7) NOT NULL CHECK(type = 'country' OR type = 'state' OR type = 'county')
	population BIGINT UNSIGNED,
	avg_income DECIMAL(12,2),
	gdp BIGINT UNSIGNED,
	UNIQUE(name, type)
	);

CREATE TABLE in_location (
	uid INT UNSIGNED NOT NULL PRIMARY KEY REFERENCES location(uid),
	enclosing_id INT UNSIGNED NOT NULL REFERENCES location(uid));

CREATE TABLE condition_name (
	condition_id INT UNSIGNED NOT NULL,
	name VARCHAR(256) NOT NULL,
	PRIMARY KEY(condition_id, name)
	);

CREATE TABLE datapoint (
	condition_id INT UNSIGNED NOT NULL REFERENCES condition_name(condition_id),
	location_id INT UNSIGNED NOT NULL REFERENCES location(uid),
	prevalence BIGINT UNSIGNED,
	incidence BIGINT UNSIGNED,
	mortality BIGINT UNSIGNED,
	year SMALLINT UNSIGNED NOT NULL,
	min_age TINYINT UNSIGNED NOT NULL,
	max_age TINYINT UNSIGNED NOT NULL,
	gender CHAR(6) NOT NULL CHECK(gender = 'male' OR gender = 'female' OR gender = 'all'),
	race_ethnicity VARCHAR(128) NOT NULL,
	PRIMARY KEY(condition_id, location_id, year, min_age, max_age, gender, race_ethnicity)
	);

CREATE TRIGGER in_restriction 
	BEFORE INSERT OR UPDATE ON in_location
	REFERENCING NEW TABLE AS new_in 
	WHEN NOT EXISTS (SELECT * FROM location AS l1, location AS l2, new_in
		WHERE l1.uid = new_in.uid AND l2.uid = new_in.enclosing_ID
		AND ((l1.type = 'state' AND l2.type = 'state') 
			OR (l1.type = 'country' AND l2.type = 'country') 
			OR (l1.type = 'county' AND l2.type = 'county')
		 	OR (l1.type = 'country' AND l2.type = 'state') 
		 	OR (l1.type = 'country' AND l2.type = 'county') 
		 	OR (l1.type = 'state' AND l2.type = 'county'))
		);
