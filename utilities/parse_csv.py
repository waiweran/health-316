import psycopg2
import time

def loadConditions(filename, column_num):
	print("Loading Conditions:")
	conn = psycopg2.connect("dbname=health")
	c = conn.cursor()
	conditions = set(readColumns(filename, {"conditions": column_num})["conditions"])
	prevProgress = -1
	index = 0
	startTime = time.time()
	for cond in conditions:
		cond_id = getConditionID(cond)
		if cond_id == None:
			c.execute("SELECT uid FROM condition")
			uidlist = c.fetchall()
			uid = makeUID(uidlist)
			c.execute("INSERT INTO condition VALUES (%s)", (uid,))
			c.execute("INSERT INTO condition_name VALUES (%s, %s)", (cond, uid))
			conn.commit()
		progress = round(index*100/len(conditions), 1)
		barsize = int(progress/2)
		timeLeft = int((time.time() - startTime)*(len(conditions)/(index+1) - 1))
		minsLeft = timeLeft // 60
		secsLeft = timeLeft % 60
		if(progress > prevProgress):
			print("Progress: |" + "█"*(barsize) + "-"*(50-barsize) + "| " + str(progress) + "% Time Remaining: " + str(minsLeft) + " minutes " + str(secsLeft) + " seconds          ", end="\r")
			prevProgress = progress
		index = index + 1
	print("Progress: |" + "█"*50 + "| 100% Time Remaining: 0 minutes 0 seconds                  ")
	c.close()
	conn.close()

def loadDataPoints(locations, location_type, conditions, years, values, data_type, pop_scaled, min_ages=[-1], max_ages=[-1], genders=['all'], race_ethnicities=['all']):
	print("Loading Datapoints:")

	condition_list = list(conditions)
	location_list = list(locations)
	value_list = list(values)
	year_list = list(years)
	minage_list = list(min_ages)
	maxage_list = list(max_ages)
	gender_list = list(genders)
	ethn_list = list(race_ethnicities)

	length = max(len(locations), len(conditions), len(years), len(min_ages), len(max_ages), len(genders), len(race_ethnicities))
	
	conn = psycopg2.connect("dbname=health")
	c = conn.cursor()

	prevProgress = -1
	startTime = time.time()

	for i in range(0, length):	
		try:
			cond_id = getConditionID(condition_list[-1])
			if i < len(condition_list):
				cond_id = getConditionID(condition_list[i])
			loc_id = getLocationID(location_list[-1], location_type)
			if i < len(location_list):
				loc_id = getLocationID(location_list[i], location_type)
			val = value_list[-1]
			if i < len(value_list):
				val = value_list[i]
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

			c.execute("INSERT INTO datapoint VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (cond_id, loc_id, val, data_type, pop_scaled, year, minage, maxage, gen, ethn))

		except:
			print("Data Error: Skipping Entry " + str(i))

		progress = round(i*100/len(conditions), 1)
		barsize = int(progress/2)
		timeLeft = int((time.time() - startTime)*(len(conditions)/(i+1) - 1))
		minsLeft = timeLeft // 60
		secsLeft = timeLeft % 60
		if(progress > prevProgress):
			print("Progress: |" + "█"*(barsize) + "-"*(50-barsize) + "| " + str(progress) + "% Time Remaining: " + str(minsLeft) + " minutes " + str(secsLeft) + " seconds          ", end="\r")
			prevProgress = progress

	print("Progress: |" + "█"*50 + "| 100% Time Remaining: 0 minutes 0 seconds                  ")
	conn.commit()
	c.close()
	conn.close()

def readColumns(filename, column_nums):
	output = dict()
	for name, num in column_nums.items():
		output[name] = list()
	index = 0
	with open(filename, 'r') as file:
		header = file.readline()
		for row in file:
			cells = split(row)
			for name, num in column_nums.items():
				output[name].append(cells[num - 1])
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

def split(row):
	output = list()
	start = 0
	while True:
		comma = row.index(',', start)
		output.append(row[start:comma])
		start = comma + 1
		if row[start] == '"':
			quote = row.index('"', start + 1)
			output.append(row[start+1:quote])
			start = quote + 2
		if row.find(',', start) < 0:
			output.append(row[start:])
			return output



