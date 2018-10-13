dbname=health
dropdb $dbname
createdb $dbname
psql health -af scripts/create.sql
python load.py >load.sql
psql $dbname -af load.sql
rm load.sql
psql $dbname -af scripts/Queries.sql >test-sample.out
echo "hot damn"
