import psycopg2

conn = psycopg2.connect("dbname=health")
c = conn.cursor()

c.execute("SELECT * FROM location")
print(c.fetchone())

conn.commit()
c.close()
conn.close()
