#!/bin/bash

# ls -l
# ls -l docker-venv
# source docker-venv/bin/activate

# # cd .docker-venv/bin
# ls -l ./docker-venv/bin/activate
# # source activate
# # #gunicorn app.src.main:app -w 1 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:80 --timeout 1000
# # cd - 
pwd
ls -l
uvicorn app.src.main:app --host 0.0.0.0 --port 8000 --reload --reload-include '*.py' --workers 1
