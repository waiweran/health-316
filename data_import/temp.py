import psycopg2

conn = psycopg2.connect("dbname=health")
c = conn.cursor()
with open("state_cancer_incidence.csv") as file_in:
	with open("state_cancer_incidence_2.csv", "w") as file_out:
		file_out.write(file_in.readline())
		for line in file_in:
			location = line.split(',')[0]
			c.execute("SELECT * FROM location WHERE name = %s", (location,))
			if not c.fetchone() == None:
				file_out.write(line)
