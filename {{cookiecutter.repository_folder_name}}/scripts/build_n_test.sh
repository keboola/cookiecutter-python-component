#!/bin/sh
set -e

ruff check
python -m pytest tests/ --tb=short -q
