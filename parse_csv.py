#import psycopg2


def importConditions(filename, column_num):
	conditions = list()
	with open(filename, 'r') as file:
		header = file.readline()
		for line in file:
			conditions.append(line.split(',')[column_num - 1])

	for cond in conditions:
		cond_id = getConditionID(cond)
		if cond_id == None:
			conn = psycopg2.connect("dbname=health")
			c = conn.cursor()
			c.execute("SELECT uid FROM condition")
			uid = makeUID(c.fetchall())
			c.execute("INSERT INTO condition VALUES (%s)", (uid))
			c.execute("INSERT INTO condition_name VALUES (%s, %s)", (uid, cond))
			conn.commit()
			c.close()
			conn.close()



def importDataVals(filename, location_col, location_type, condition_col, mortality_col, year_col)
	with open(filename, 'r') as file:
		header = file.readline()
		for line in file:
			cells = line.split(',')
			loc_id = getLocationID(cells[location_col], location_type)
			cond_id = getConditionID(cells[condition_col])
			mort = int(cells[mortality_col])
			year = int(cells[year_col])
			conn = psycopg2.connect("dbname=health")
			c = conn.cursor()
			c.execute("INSERT INTO datapoint VALUES (%s, %s, NULL, NULL, %s, %s, NULL, NULL, NULL, NULL)", (cond_id, loc_id, mort, year))
			conn.commit()
			c.close()
			conn.close()



def getConditionID(name):
	conn = psycopg2.connect("dbname=health")
	c = conn.cursor()
	c.execute("SELECT condition_id FROM condition_name WHERE name = %s", (name))
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
	while formatUID(i) in existingIDs:
		i = i + 1
	return formatUID(i)

def formatUID(idval):
	idlen = len(str(idval))
	return (4 - idlen)*'0' + str(idval)
