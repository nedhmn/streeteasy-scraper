#!/usr/bin/env bash

set -e
set -x

python packages/db/scripts/init_db.py
python apps/address_scraper/scripts/run_address_scraper.py
