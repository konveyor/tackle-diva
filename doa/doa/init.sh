# env variables to be injected:
# - DB_HOST
# - SQL ROOT
# - PGPASSWORD
psql -h ${DB_HOST} -U postgres -f ${SQL_ROOT}/init_db.sql
psql -h ${DB_HOST} -U postgres -d jrvstrading -f ${SQL_ROOT}/schema.sql
