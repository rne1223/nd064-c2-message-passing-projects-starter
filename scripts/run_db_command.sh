# Usage: pass in the DB container ID as the argument

# Set database configurations
export CT_DB_USERNAME=ct_admin
export CT_DB_NAME=geoconnections

# echo $1
# echo $2

# cat ~/udaconnect/db/dropDB.sql | kubectl exec -i $1 -- bash -c "psql -U $CT_DB_USERNAME -d $CT_DB_NAME"

cat ~/udaconnect/db/2020-08-15_init-db.sql | kubectl exec -i $1 -- bash -c "psql -U $CT_DB_USERNAME -d $CT_DB_NAME"

cat ~/udaconnect/db/udaconnect_public_person.sql | kubectl exec -i $1 -- bash -c "psql -U $CT_DB_USERNAME -d $CT_DB_NAME"

cat ~/udaconnect/db/udaconnect_public_location.sql | kubectl exec -i $1 -- bash -c "psql -U $CT_DB_USERNAME -d $CT_DB_NAME"
