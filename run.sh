dropdb health
createdb health
psql health -af scripts/create.sql
psql health -af scripts/load.sql
python3 load.py