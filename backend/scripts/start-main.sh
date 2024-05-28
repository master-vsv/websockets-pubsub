#!/bin/bash

pwd
ls -l
python scripts/compile.py
uvicorn app.src.main:app --host 0.0.0.0 --port 8000 --reload --reload-include '*.py' --workers 1
