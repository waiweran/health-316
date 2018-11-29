import psycopg2

def getDataTypes(condition_name):
    '''Lists the types of data in the database for the given condition'''
    conn = psycopg2.connect("dbname=health")
    c = conn.cursor()
    c.execute('''
        SELECT DISTINCT type, name
        FROM datapoint, condition_name
        WHERE datapoint.condition_id = condition_name.condition_id
        AND condition_name.name = %s
    ''', (condition_name,))
    results = c.fetchall()
    c.close()
    conn.close()
    types, names = zip(*results)
    return types

def getMapData(condition_name, data_type):
    '''Gets a dataset in map plotting format given a condition name and a data type'''
    conn = psycopg2.connect("dbname=health")
    c = conn.cursor()
    c.execute('''
        SELECT location.name, datapoint.value
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
