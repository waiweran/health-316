import psycopg2

def getAllConditions():
    '''Lists all conditions available in the database'''
    conn = psycopg2.connect("dbname=health")
    c = conn.cursor()
    c.execute('''SELECT name FROM condition_name ORDER BY name;''')
    results = c.fetchall()
    c.close()
    conn.close()
    output = [val[0] for val in results]
    return output


def getDataTypes(condition_name):
    '''Lists the types of data in the database for the given condition'''
    conn = psycopg2.connect("dbname=health")
    c = conn.cursor()
    c.execute('''
        SELECT DISTINCT type, name
        FROM datapoint, condition_name
        WHERE datapoint.condition_id = condition_name.condition_id
        AND condition_name.name = %s;
    ''', (condition_name,))
    results = c.fetchall()
    c.close()
    conn.close()
    types, names = zip(*results)
    return types

def getDataYears(condition_name, data_type):
    '''Lists the years that have data for the given condition and data type'''
    conn = psycopg2.connect("dbname=health")
    c = conn.cursor()
    c.execute('''
        SELECT DISTINCT year
        FROM datapoint, condition_name
        WHERE datapoint.condition_id = condition_name.condition_id
        AND condition_name.name = %s
        AND datapoint.type = %s
        ORDER BY year DESC;
    ''', (condition_name, data_type))
    results = c.fetchall()
    c.close()
    conn.close()
    output = [val[0] for val in results]
    return output

def getDataAges(condition_name, data_type):
    '''Lists the age ranges for the given condition and data type'''
    conn = psycopg2.connect("dbname=health")
    c = conn.cursor()
    c.execute('''
        SELECT DISTINCT min_age, max_age
        FROM datapoint, condition_name
        WHERE datapoint.condition_id = condition_name.condition_id
        AND condition_name.name = %s
        AND datapoint.type = %s
        ORDER BY min_age;
    ''', (condition_name, data_type))
    results = c.fetchall()
    c.close()
    conn.close()
    output = [val[0] for val in results]
    return output

def getDataGenders(condition_name, data_type):
    '''Lists the genders for the given condition and data type'''
    conn = psycopg2.connect("dbname=health")
    c = conn.cursor()
    c.execute('''
        SELECT DISTINCT gender
        FROM datapoint, condition_name
        WHERE datapoint.condition_id = condition_name.condition_id
        AND condition_name.name = %s
        AND datapoint.type = %s
        ORDER BY gender;
    ''', (condition_name, data_type))
    results = c.fetchall()
    c.close()
    conn.close()
    output = [val[0] for val in results]
    return output

def getDataRaces(condition_name, data_type, ):
    '''Lists the races/ethnicities for the given condition and data type'''
    conn = psycopg2.connect("dbname=health")
    c = conn.cursor()
    c.execute('''
        SELECT DISTINCT race_ethnicity
        FROM datapoint, condition_name
        WHERE datapoint.condition_id = condition_name.condition_id
        AND condition_name.name = %s
        AND datapoint.type = %s
        ORDER BY race_ethnicity;
    ''', (condition_name, data_type))
    results = c.fetchall()
    c.close()
    conn.close()
    output = [val[0] for val in results]
    return output

def getMapData(condition_name, data_type, year, min_age=-1, max_age=-1, gender='all', race_ethnicity='all'):
    '''Gets a dataset in map plotting format given a condition name and a data type'''
    conn = psycopg2.connect("dbname=health")
    c = conn.cursor()
    c.execute('''
        SELECT location.abbr, datapoint.value
        FROM datapoint, condition_name, location
        WHERE datapoint.condition_id = condition_name.condition_id
        AND datapoint.location_id = location.uid
        AND condition_name.name = %s
        AND datapoint.type = %s
        AND datapoint.year = %s
        AND datapoint.min_age = %s
        AND datapoint.max_age = %s
        AND datapoint.gender = %s
        AND datapoint.race_ethnicity = %s;
    ''', (condition_name, data_type, year, min_age, max_age, gender, race_ethnicity))
    results = c.fetchall()
    c.close()
    conn.close()
    locations, values = zip(*results)
    return locations, values

def updateHistory(condition_name):
    conn = psycopg2.connect("dbname=health")
    c = conn.cursor()
    c.execute('''
        SELECT condition_id
        FROM condition_name
        WHERE condition_name.name = %s;
    ''', (condition_name,))
    results = c.fetchone()
    c.execute('''
        INSERT INTO history VALUES(NOW(), %s)
    ''', (results[0]))
    c.close()
    conn.close()

