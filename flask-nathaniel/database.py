import psycopg2

state_codes = {
    'Alabama':'AL',
    'Alaska':'AK',
    'Arizona':'AZ',
    'Arkansas':'AR',
    'California':'CA',
    'Colorado':'CO',
    'Connecticut':'CT',
    'Delaware':'DE',
    'Florida':'FL',
    'Georgia':'GA',
    'Hawaii':'HI',
    'Idaho':'ID',
    'Illinois':'IL',
    'Indiana':'IN',
    'Iowa':'IA',
    'Kansas':'KS',
    'Kentucky':'KY',
    'Louisiana':'LA',
    'Maine':'ME',
    'Maryland':'MD',
    'Massachusetts':'MA',
    'Michigan':'MI',
    'Minnesota':'MN',
    'Mississippi':'MS',
    'Missouri':'MO',
    'Montana':'MT',
    'Nebraska':'NE',
    'Nevada':'NV',
    'New Hampshire':'NH',
    'New Jersey':'NJ',
    'New Mexico':'NM',
    'New York':'NY',
    'North Carolina':'NC',
    'North Dakota':'ND',
    'Ohio':'OH',
    'Oklahoma':'OK',
    'Oregon':'OR',
    'Pennsylvania':'PA',
    'Rhode Island':'RI',
    'South Carolina':'SC',
    'South Dakota':'SD',
    'Tennessee':'TN',
    'Texas':'TX',
    'Utah':'UT',
    'Vermont':'VT',
    'Virginia':'VA',
    'Washington':'WA',
    'West Virginia':'WV',
    'Wisconsin':'WI',
    'Wyoming':'WY',
    'District of Columbia':'DC',
}

def getDataTypes(condition_name):
    '''Lists the types of data in the database for the given condition'''
    print(condition_name)
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
    loc_names, values = zip(*results)
    locations = [state_codes[name] for name in loc_names]
    return locations, values
