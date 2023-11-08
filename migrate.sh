#!/bin/bash
echo "Waiting for PostgreSQL to be ready..."
./wait-for-it.sh postgres:5432 -t 30

echo "Running migrations..."
DB=$LOCAL_DEV_DB alembic -c /alembic.ini upgrade head
DB=$LOCAL_TEST_DB alembic -c /alembic.ini upgrade head
echo "Migrations completed."

PGPASSWORD=postgres psql -U postgres -h postgres_container -p 5432 -c "\dt" devdb

# Loads data into client_family - specific to application
HAS_ROWS=$(PGPASSWORD=postgres psql -U postgres -h postgres_container -p 5432 -t -c "SELECT 1 FROM client_family LIMIT 1;" devdb | tr -d '[:space:]')
echo "$HASROWS"
if [ -z "$HAS_ROWS" ]; then
  echo "Loading dummy data into devdb..."
    echo "Loading dummy data into devdb..."
  PGPASSWORD=postgres psql -U postgres -h postgres_container -p 5432 devdb <<-EOSQL
    \copy client_family FROM '/dummy-data.csv' WITH CSV
EOSQL
  echo "Loaded dummy data into devdb."
else
  echo "Table client_family already exists and/or has data. Skipping dummy data loading."
fi