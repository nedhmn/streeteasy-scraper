#!/usr/bin/env bash

set -e
set -x

python scripts/run_async_submit_jobs.py
python scripts/run_async_process_jobs.py
