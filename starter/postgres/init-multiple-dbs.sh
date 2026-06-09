#!/bin/bash
# Creates one database (and a dedicated owner role) per entry listed in
# POSTGRES_MULTIPLE_DATABASES. Runs once, on the very first container start,
# via the official postgres image's /docker-entrypoint-initdb.d hook.
#
# Entry format (comma-separated):
#   dbname:user:password   -> creates role `user` owning database `dbname`
#   dbname                 -> database owned by the default POSTGRES_USER
#
# Example:
#   POSTGRES_MULTIPLE_DATABASES="management:mgmt:mgmtpass,streaming:stream:streampass"

set -euo pipefail

create_db_and_user() {
	local entry="$1"
	local db user pass

	db="${entry%%:*}"
	local rest="${entry#*:}"

	if [ "$rest" != "$entry" ]; then
		user="${rest%%:*}"
		pass="${rest#*:}"
	else
		# No user/password supplied: database owned by the superuser.
		user="$POSTGRES_USER"
		pass=""
	fi

	echo "  -> ensuring database '$db' (owner '$user')"

	psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
		DO \$\$
		BEGIN
		   IF '$user' <> '$POSTGRES_USER' AND NOT EXISTS (
		      SELECT FROM pg_roles WHERE rolname = '$user'
		   ) THEN
		      CREATE ROLE "$user" LOGIN PASSWORD '$pass';
		   END IF;
		END
		\$\$;

		SELECT 'CREATE DATABASE "$db" OWNER "$user"'
		WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$db')\gexec

		-- Confine the database to its owner: no other service role can connect.
		REVOKE CONNECT ON DATABASE "$db" FROM PUBLIC;
		GRANT ALL PRIVILEGES ON DATABASE "$db" TO "$user";
	EOSQL
}

if [ -z "${POSTGRES_MULTIPLE_DATABASES:-}" ]; then
	echo "POSTGRES_MULTIPLE_DATABASES not set, nothing to do."
	exit 0
fi

echo "Creating databases from POSTGRES_MULTIPLE_DATABASES..."
IFS=',' read -ra ENTRIES <<<"$POSTGRES_MULTIPLE_DATABASES"
for entry in "${ENTRIES[@]}"; do
	# trim surrounding whitespace
	entry="$(echo "$entry" | xargs)"
	[ -z "$entry" ] && continue
	create_db_and_user "$entry"
done
echo "Done."
