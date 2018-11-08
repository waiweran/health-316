cd ..
dropdb health
createdb health
psql health -af scripts/create.sql
psql health -af scripts/load.sql
python3 parse_csv.py
./flask-nathaniel/run_dev.sh
