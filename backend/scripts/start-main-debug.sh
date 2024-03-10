#!/bin/bash

pwd
ls -l
python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m uvicorn app.src.main:app --host 0.0.0.0 --port 80 --reload --workers 1
