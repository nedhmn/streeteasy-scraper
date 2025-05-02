#!/usr/bin/env bash

set -e
set -x

mypy apps packages
ruff check apps packages
ruff format apps packages --check
