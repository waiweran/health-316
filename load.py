from utilities import parse_csv as csv

csv.loadConditions("data_import/state_common_mortality.csv", 3)
cols = csv.readColumns("data_import/state_common_mortality.csv", {"locations": 4, "conditions": 3, "years": 1, "values": 5})
csv.loadDataPoints(locations=cols["locations"], location_type='state', conditions=cols["conditions"], years=cols["years"], values=cols["values"], data_type="Mortality", pop_scaled=False)

csv.loadConditions("data_import/state_heartdisease.csv", 6)
cols = csv.readColumns("data_import/state_heartdisease.csv", {"locations": 3, "conditions": 6, "years": 1, "values": 8, "genders": 14, "ethn": 16})
csv.loadDataPoints(locations=cols["locations"], location_type='state', conditions=cols["conditions"], years=cols["years"], values=cols["values"], data_type="Mortality per 100,000", pop_scaled=True, genders=cols["genders"], race_ethnicities=cols["ethn"])

csv.loadConditions("data_import/state_cancer_incidence.csv", 10)
cols = csv.readColumns("data_import/state_cancer_incidence.csv", {"locations": 1, "conditions": 10, "years": 11, "values": 4, "genders": 9, "ethn": 8})
csv.loadDataPoints(locations=cols["locations"], location_type='state', conditions=cols["conditions"], years=cols["years"], values=cols["values"], data_type="Age Adjusted Incidence (rate)", pop_scaled=True, genders=cols["genders"], race_ethnicities=cols["ethn"])

csv.loadConditions("data_import/state_cancer_mortality.csv", 10)
cols = csv.readColumns("data_import/state_cancer_mortality.csv", {"locations": 1, "conditions": 10, "years": 11, "values": 4, "genders": 9, "ethn": 8})
csv.loadDataPoints(locations=cols["locations"], location_type='state', conditions=cols["conditions"], years=cols["years"], values=cols["values"], data_type="Age Adjusted Mortality (rate)", pop_scaled=True, genders=cols["genders"], race_ethnicities=cols["ethn"])
