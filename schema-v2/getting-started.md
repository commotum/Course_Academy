# Getting started

## 1. Database creation

Run as `jake` in Bash. The FireCuda partition `/dev/nvme1n1p1` is mounted at
`/media/jake/SSD`. PostgreSQL data and WAL will live in
`/media/jake/SSD/EDB/math/postgres`. This uses the installed PostgreSQL 15 binaries,
with [local authentication](https://www.postgresql.org/docs/15/auth-trust.html)
through a private Unix socket and no TCP listener.

In terminal 1, run once:

```bash
set -e
umask 077

test "$(findmnt -n -o UUID --target /media/jake/SSD)" = \
  3e6801f5-379d-45c6-ab0d-2d8b7d3541e5

cd /home/jake/Developer/EDB
cargo build --locked --release --bin edb

edb_math_pg=/usr/local/MATLAB/R2025b/sys/postgresql/glnxa64/PostgreSQL/bin
edb_math_data=/media/jake/SSD/EDB/math/postgres
edb_math_run=/tmp/edb-math

mkdir -p "$(dirname "$edb_math_data")" "$edb_math_run"
chmod 700 "$edb_math_run"

"$edb_math_pg/initdb" -D "$edb_math_data" \
  --username=edb_admin --encoding=UTF8 --locale=C \
  --auth-local=trust --auth-host=reject

cat >> "$edb_math_data/postgresql.conf" <<'CONF'
listen_addresses = ''
port = 55432
unix_socket_directories = '/tmp/edb-math'
unix_socket_permissions = 0700
CONF

"$edb_math_pg/pg_ctl" -D "$edb_math_data" \
  -l /media/jake/SSD/EDB/math/postgres.log -w start

"$edb_math_pg/psql" -X -h "$edb_math_run" -p 55432 \
  -U edb_admin -d postgres -v ON_ERROR_STOP=1 <<'SQL'
CREATE ROLE edb_writer LOGIN;
CREATE ROLE edb_peer LOGIN;
CREATE DATABASE math OWNER edb_admin;
SQL

export EDB_POSTGRES_URL="host=$edb_math_run port=55432 dbname=math user=edb_admin sslmode=disable options='-c search_path=public'"

target/release/edb install --writer-role edb_writer --peer-role edb_peer
target/release/edb create --database math
target/release/edb status --database math
```

Start the writer in the same terminal. Wait for `READY` and leave it running:

```bash
export EDB_POSTGRES_URL="host=$edb_math_run port=55432 dbname=math user=edb_writer sslmode=disable options='-c search_path=public'"

target/release/edb transactor \
  --database math \
  --endpoint "$edb_math_run/writer.sock"
```

## 2. Source bootstrapping

In terminal 2:

```bash
set -e
cd /home/jake/Developer/EDB

export EDB_DATABASE=math
export EDB_ENDPOINT=/tmp/edb-math/writer.sock
export EDB_POSTGRES_URL="host=/tmp/edb-math port=55432 dbname=math user=edb_peer sslmode=disable options='-c search_path=public'"

target/release/edb transact \
  --database "$EDB_DATABASE" \
  --endpoint "$EDB_ENDPOINT" \
  --request-key bootstrap-jake \
  --source '"jake"' \
  --file - <<'EDN'
[{:db/id "jake"
  :db/ident :person/jake
  :db/doc "Jake"}]
EDN

target/release/edb pull \
  --database "$EDB_DATABASE" \
  --entity ':person/jake' \
  --file - <<'EDN'
[:db/id :db/ident :db/doc]
EDN
```

The commit reports `:edb/committed true`. Pull returns `:person/jake` and `"Jake"`.
Use `--source ':person/jake'` for subsequent schema transactions. Continue in
terminal 2 with terminal 1's writer running.

## 3. Schema installation
