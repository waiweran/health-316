from utilities import parse_csv as csv

csv.loadConditions("data_import/state_common_mortality.csv", 3)
cols = csv.readColumns("data_import/state_common_mortality.csv", {"locations": 4, "conditions": 3, "years": 1, "mortalities": 5})
csv.loadDataPoints(locations=cols["locations"], location_type='state', conditions=cols["conditions"], years=cols["years"], mortalities=cols["mortalities"])

csv.loadConditions("data_import/state_heartdisease.csv", 6)
cols = csv.readColumns("data_import/state_common_mortality.csv", {"locations": 3, "conditions": 6, "years": 1, "mortalities": 8, "genders": 14, "ethn": 16})
csv.loadDataPoints(locations=cols["locations"], location_type='state', conditions=cols["conditions"], years=cols["years"], mortalities=cols["mortalities"], genders=cols["genders"], race_ethnicities=cols["ethn"])
