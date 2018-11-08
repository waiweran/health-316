import psycopg2

def loadConditions(filename, column_num):
	for cond in readColumn(filename, column_num):
		cond_id = getConditionID(cond)
		if cond_id == None:
			conn = psycopg2.connect("dbname=health")
			c = conn.cursor()
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
	
	while len(condition_list) < length:
		condition_list.append(condition_list[-1])
	while len(location_list) < length:
		location_list.append(location_list[-1])
	while len(prevalence_list) < length:
		prevalence_list.append(prevalence_list[-1])
	while len(incidence_list) < length:
		incidence_list.append(incidence_list[-1])
	while len(mortality_list) < length:
		mortality_list.append(mortality_list[-1])
	while len(year_list) < length:
		year_list.append(year_list[-1])
	while len(minage_list) < length:
		minage_list.append(minage_list[-1])
	while len(maxage_list) < length:
		maxage_list.append(maxage_list[-1])
	while len(gender_list) < length:
		gender_list.append(gender_list[-1])
	while len(ethn_list) < length:
		ethn_list.append(ethn_list[-1])

	for i in range(0, length):	
		cond_id = getConditionID(condition_list[i])
		loc_id = getLocationID(location_list[i], location_type)
		prev = prevalence_list[i]
		inc = incidence_list[i]
		mort = mortality_list[i]
		year = year_list[i]
		minage = minage_list[i]
		maxage = maxage_list[i]
		gen = gender_list[i]
		ethn = ethn_list[i]

		conn = psycopg2.connect("dbname=health")
		c = conn.cursor()
		c.execute("INSERT INTO datapoint VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (cond_id, loc_id, prev, inc, mort, year, minage, maxage, gen, ethn))
		conn.commit()
		c.close()
		conn.close()

def readColumn(filename, column_num):
	cells = list()
	with open(filename, 'r') as file:
		header = file.readline()
		for row in file:
			 cells.append(row.split(',')[column_num - 1])
	return cells

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
loadDataPoints(locations=readColumn("mort_data.csv", 4), location_type='state', conditions=readColumn("mort_data.csv", 3), years=readColumn("mort_data.csv", 1), mortalities=readColumn("mort_data.csv", 5))
