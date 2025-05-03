#!/usr/bin/env bash

set -e
set -x

python apps/streeteasy_scraper/scripts/run_async_submit_jobs.py
python apps/streeteasy_scraper/scripts/run_async_process_jobs.py
