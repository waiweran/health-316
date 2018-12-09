import psycopg2

def getAllConditions():
    '''Lists all conditions available in the database'''
    conn = psycopg2.connect("dbname=health")
    c = conn.cursor()
    c.execute('''SELECT name FROM condition_name;''')
    results = c.fetchall()
    c.close()
    conn.close()
    return list(results[0])


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
        SELECT DISTINCT datapoint.year
        FROM datapoint, condition_name
        WHERE datapoint.condition_id = condition_name.condition_id
        AND condition_name.name = %s
        AND datapoint.type = %s;
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
        SELECT DISTINCT datapoint.min_age, datapoint.max_age
        FROM datapoint, condition_name
        WHERE datapoint.condition_id = condition_name.condition_id
        AND condition_name.name = %s
        AND datapoint.type = %s;
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
        SELECT DISTINCT datapoint.gender
        FROM datapoint, condition_name
        WHERE datapoint.condition_id = condition_name.condition_id
        AND condition_name.name = %s
        AND datapoint.type = %s;
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
        SELECT DISTINCT datapoint.race_ethnicity
        FROM datapoint, condition_name
        WHERE datapoint.condition_id = condition_name.condition_id
        AND condition_name.name = %s
        AND datapoint.type = %s;
    ''', (condition_name, data_type))
    results = c.fetchall()
    c.close()
    conn.close()
    output = [val[0] for val in results]
    return output

def getMapData(condition_name, data_type):
    '''Gets a dataset in map plotting format given a condition name and a data type'''
    conn = psycopg2.connect("dbname=health")
    c = conn.cursor()
    c.execute('''
        SELECT location.abbr, datapoint.value
        FROM datapoint, condition_name, location
        WHERE datapoint.condition_id = condition_name.condition_id
        AND datapoint.location_id = location.uid
        AND condition_name.name = %s
        AND datapoint.type = %s;
    ''', (condition_name, data_type))
    results = c.fetchall()
    c.close()
    conn.close()
    locations, values = zip(*results)
    return locations, values