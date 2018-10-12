dropdb health
createdb health
psql health -af scripts/create.sql
python load.py >load.sql
psql health -af load.sql
rm load.sql
psql health -af scripts/Queries.sql >test-sample.out
echo "hot damn"