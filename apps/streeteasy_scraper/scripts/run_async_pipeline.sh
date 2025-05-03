#!/usr/bin/env bash

set -e
set -x

python run_async_submit_jobs.py
python run_async_process_jobs.py
