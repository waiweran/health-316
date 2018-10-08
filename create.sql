CREATE TABLE location (
	uid INT UNSIGNED NOT NULL PRIMARY KEY,
	name VARCHAR(256) NOT NULL,
	population BIGINT UNSIGNED,
	avg_income DECIMAL(12,2),
	gdp BIGINT UNSIGNED
	);

CREATE TABLE country (
	country_id INT UNSIGNED NOT NULL PRIMARY KEY REFERENCES location(uid)
	);

CREATE TABLE state (
	state_id INT UNSIGNED NOT NULL PRIMARY KEY REFERENCES location(uid),
	country_id INT UNSIGNED NOT NULL REFERENCES country(country_id));

CREATE TABLE county (
	county_id INT UNSIGNED NOT NULL PRIMARY KEY REFERENCES location(uid),
	state_id INT UNSIGNED NOT NULL REFERENCES state(state_id)
	);

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