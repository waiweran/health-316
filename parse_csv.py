import psycopg2


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



def importDataVals(filename, location_col, location_type, condition_col, mortality_col, year_col):
	with open(filename, 'r') as file:
		header = file.readline()
		for line in file:
			cells = line.split(',')
			loc_id = getLocationID(cells[location_col - 1], location_type)
			cond_id = getConditionID(cells[condition_col - 1])
			mort = int(cells[mortality_col - 1])
			year = int(cells[year_col - 1])
			conn = psycopg2.connect("dbname=health")
			c = conn.cursor()
			c.execute("INSERT INTO datapoint VALUES (%s, %s, NULL, NULL, %s, %s, NULL, NULL, NULL, NULL)", (cond_id, loc_id, mort, year))
			conn.commit()
			c.close()
			conn.close()



def getConditionID(name):
	print("<<" + name + ">>")
	conn = psycopg2.connect("dbname=health")
	c = conn.cursor()
	c.execute("SELECT condition_id FROM condition_name WHERE name = %s", ("poop"))
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


importConditions("mort_data.csv", 3)
importDataVals("mort_data.csv", 4, 'state', 3, 5, 1)
