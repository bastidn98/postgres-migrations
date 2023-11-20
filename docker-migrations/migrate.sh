#!/bin/bash
echo "Waiting for PostgreSQL to be ready..."
./wait-for-it.sh db:5432 -t 5

echo "Running migrations..."
DB=$PROD_DBNAME HOST=$PROD_HOST alembic -c ./alembic.ini upgrade head
echo "Migrations completed."

# PGPASSWORD=postgres psql -U postgres -h db -c "\dt" $DB
