#!/bin/bash
##### Creates databases defined by LOCAL_DEV_DB and LOCAL_TEST_DB
echo 'RUNNING SETUP'

set -e

until PGPASSWORD=$POSTGRES_PASSWORD psql  -v ON_ERROR_STOP=1 --username postgres -c '\l'; do
    echo "PostgreSQL is unavailable - sleeping"
    sleep 1
done
echo "PostgreSQL is up and running"

# Create development and test databases
psql -v ON_ERROR_STOP=1 --username postgres <<-EOSQL
    CREATE DATABASE "$LOCAL_DEV_DB";
    CREATE DATABASE "$LOCAL_TEST_DB";
EOSQL
echo "Created "$LOCAL_DEV_DB" and "$LOCAL_TEST_DB""

PGPASSWORD=$POSTGRES_PASSWORD psql  -v ON_ERROR_STOP=1 --username postgres -c '\l'
