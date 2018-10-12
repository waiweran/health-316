dropdb health
createdb health
psql health -af create.sql
python load.py