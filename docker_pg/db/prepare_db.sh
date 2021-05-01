#!/bin/sh
set -e

/opt/code/db/start_postgres.sh

echo 'Creating Schema'
python3 -m nanotwitter_pg.init_db

/opt/code/db/stop_postgres.sh
