import psycopg2

def loadConditions(filename, column_num):
	conn = psycopg2.connect("dbname=health")
	c = conn.cursor()
	for name, cond in readColumn(filename, {"conditions": column_num}):
		cond_id = getConditionID(cond)
		if cond_id == None:
			c.execute("SELECT uid FROM condition")
			uidlist = c.fetchall()
			uid = makeUID(uidlist)
			c.execute("INSERT INTO condition VALUES (%s)", (uid,))
			c.execute("INSERT INTO condition_name VALUES (%s, %s)", (cond, uid))
			conn.commit()
	c.close()
	conn.close()

def loadDataPoints(locations, location_type, conditions, years, prevalences=[None], incidences=[None], mortalities=[None], min_ages=[-1], max_ages=[-1], genders=['all'], race_ethnicities=['all']):
	condition_list = list(conditions)
	location_list = list(locations)
	prevalence_list = list(prevalences)
	incidence_list = list(incidences)
	mortality_list = list(mortalities)
	year_list = list(years)
	minage_list = list(min_ages)
	maxage_list = list(max_ages)
	gender_list = list(genders)
	ethn_list = list(race_ethnicities)

	length = max(len(locations), len(conditions), len(years), len(min_ages), len(max_ages), len(genders), len(race_ethnicities))
	
	conn = psycopg2.connect("dbname=health")
	c = conn.cursor()

	for i in range(0, length):	
		cond_id = getConditionID(condition_list[-1])
		if i < len(condition_list):
			cond_id = getConditionID(condition_list[i])
		loc_id = getLocationID(location_list[-1], location_type)
		if i < len(location_list):
			loc_id = getLocationID(location_list[i], location_type)
		prev = prevalence_list[-1]
		if i < len(prevalence_list):
			prev = prevalence_list[i]
		inc = incidence_list[-1]
		if i < len(incidence_list):
			inc = incidence_list[i]
		mort = mortality_list[-1]
		if i < len(mortality_list):
			mort = mortality_list[i]
		year = year_list[-1]
		if i < len(year_list):
			year = year_list[i]
		minage = minage_list[-1]
		if i < len(minage_list):
			minage = minage_list[i]
		maxage = maxage_list[-1]
		if i < len(maxage_list):
			maxage = maxage_list[i]
		gen = gender_list[-1]
		if i < len(gender_list):
			gen = gender_list[i]
		ethn = ethn_list[-1]
		if i < len(ethn_list):
			ethn = ethn_list[i]

		c.execute("INSERT INTO datapoint VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (cond_id, loc_id, prev, inc, mort, year, minage, maxage, gen, ethn))

	conn.commit()
	c.close()
	conn.close()

def readColumns(filename, column_nums):
	output = dict()
	for val in column_nums:
		output.append(list())
	with open(filename, 'r') as file:
		header = file.readline()
		for row in file:
			cells = row.split(',')
			for name, num in column_nums:
				output[name] = cells[num]
	return output

def getConditionID(name):
	conn = psycopg2.connect("dbname=health")
	c = conn.cursor()
	c.execute("SELECT condition_id FROM condition_name WHERE name = %s", (name,))
	uid = c.fetchone()
	conn.commit()
	c.close()
	conn.close()
	return uid

def getLocationID(name, type):
	conn = psycopg2.connect("dbname=health")
	c = conn.cursor()
	c.execute("SELECT uid FROM location WHERE name = %s AND type = %s", (name, type))
	uid = c.fetchone()
	conn.commit()
	c.close()
	conn.close()
	return uid

def makeUID(existingIDs):
	i = 0
	while (formatUID(i),) in existingIDs:
		i = i + 1
	return formatUID(i)

def formatUID(idval):
	idlen = len(str(idval))
	return (4 - idlen)*'0' + str(idval)


loadConditions("mort_data.csv", 3)
cols = readColumns("mort_data.csv", {"locations": 4, "conditions": 3, "years": 1, "mortalities": 5})
loadDataPoints(locations=cols["locations"], location_type='state', conditions=cols["conditions"], years=cols["years"], mortalities=cols["mortalities"])
