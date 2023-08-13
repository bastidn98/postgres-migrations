#!/bin/bash
echo "Waiting for PostgreSQL to be ready..."
./wait-for-it.sh postgres:5432 -t 30

echo "Running migrations..."
DB=$LOCAL_DEV_DB alembic -c /alembic.ini upgrade head
echo "Migrations completed."

PGPASSWORD=postgres psql -U postgres -h postgres_container -p 5432 -c "\dt" devdb

echo "Loading dummy data into devdb..."
PGPASSWORD=postgres psql -U postgres -h postgres_container -p 5432 devdb <<-EOSQL
    \copy client_family FROM '/dummy-data.csv' WITH CSV
EOSQL
echo "Loaded dummy data into devdb."

# # Check if the client_family table exists and has any rows
# TABLE_EXISTS=$(psql -U postgres -d "$LOCAL_NAME_DEV" -t -c "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'client_family');")
# HAS_ROWS=$(psql -U postgres -d "$LOCAL_NAME_DEV" -t -c "SELECT EXISTS (SELECT 1 FROM client_family LIMIT 1);")

# if [ "$TABLE_EXISTS" = " t " ] && [ "$HAS_ROWS" = " f " ]; then
#   echo "Loading dummy data into devdb..."
#   psql -v ON_ERROR_STOP=1 --username postgres --dbname "$LOCAL_NAME_DEV" <<-EOSQL
#       \copy client_family FROM '/dummy-data.json' WITH CSV
#   EOSQL
#   echo "Loaded dummy data into devdb."
# else
#   echo "Table client_family already exists and has data. Skipping dummy data loading."
# fi