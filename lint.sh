#!/bin/bash
isort -rc tests/ optimization_lib.py main.py
autoflake -r --in-place --remove-unused-variables tests/ optimization_lib.py main.py
black -l 120 tests/ optimization_lib.py main.py
flake8 --max-line-length 120 tests/ optimization_lib.py main.py