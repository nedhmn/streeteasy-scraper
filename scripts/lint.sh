#!/usr/bin/env bash

set -e
set -x

mypy packages
ruff check packages
ruff format packages --check
