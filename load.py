from utilities import parse_csv as csv

csv.loadConditions("data_files/state_common_mortality.csv", 3)
cols = csv.readColumns("data_files/state_common_mortality.csv", {"locations": 4, "conditions": 3, "years": 1, "mortalities": 5})
csv.loadDataPoints(locations=cols["locations"], location_type='state', conditions=cols["conditions"], years=cols["years"], mortalities=cols["mortalities"])
