CREATE TABLE location (
	uid CHAR(32) NOT NULL PRIMARY KEY,
	name VARCHAR(256) NOT NULL,
	type CHAR(7) NOT NULL CHECK(type = 'country' OR type = 'state' OR type = 'county'),
	population BIGINT,
	avg_income DECIMAL(12,2),
	gdp BIGINT
	);

CREATE TABLE in_location (
	uid CHAR(32) NOT NULL PRIMARY KEY REFERENCES location(uid),
	enclosing_id CHAR(32) NOT NULL REFERENCES location(uid)
	);

CREATE TABLE condition (
	uid CHAR(32) NOT NULL PRIMARY KEY
	);

CREATE TABLE condition_name (
	name VARCHAR(256) NOT NULL PRIMARY KEY,
	condition_id CHAR(32) NOT NULL REFERENCES condition(uid)
	);

CREATE TABLE datapoint (
	condition_id CHAR(32) NOT NULL REFERENCES condition(uid),
	location_id CHAR(32) NOT NULL REFERENCES location(uid),
	prevalence BIGINT,
	incidence BIGINT,
	mortality BIGINT,
	year SMALLINT NOT NULL,
	min_age SMALLINT NOT NULL,
	max_age SMALLINT NOT NULL,
	gender CHAR(6) NOT NULL CHECK(gender = 'male' OR gender = 'female' OR gender = 'all'),
	race_ethnicity VARCHAR(128) NOT NULL,
	PRIMARY KEY(condition_id, location_id, year, min_age, max_age, gender, race_ethnicity)
	);
/*
CREATE FUNCTION TF_in_restriction() RETURNS TRIGGER AS $$
BEGIN
	IF NOT EXISTS (SELECT * FROM location AS l1, location AS l2
		WHERE l1.uid = NEW.uid AND l2.uid = NEW.enclosing_id
		AND ((l1.type = 'state' AND l2.type = 'state') 
			OR (l1.type = 'country' AND l2.type = 'country') 
			OR (l1.type = 'county' AND l2.type = 'county')
		 	OR (l1.type = 'country' AND l2.type = 'state') 
		 	OR (l1.type = 'country' AND l2.type = 'county') 
		 	OR (l1.type = 'state' AND l2.type = 'county'))
		) THEN
		RAISE EXCEPTION 'Invalid location hierarchy';
	END IF;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_in_restriction
	BEFORE INSERT OR UPDATE ON in_location
	FOR EACH ROW
	EXECUTE PROCEDURE TF_in_restriction();
*/

