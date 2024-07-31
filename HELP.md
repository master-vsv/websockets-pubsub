

# Help

## venv

python -m venv venv
venv\Scripts\activate
venv\Scripts\deactivate

## pip

pip freeze > backend/requirements.txt
pip install -r backend/requirements.txt
pip uninstall -r requirements.txt -y
pip download -r requirements.txt -d path_to_the_folder

## Git
git reset --hard HEAD       (going back to HEAD)
git reset --hard HEAD~1     (going back to the commit before HEAD)
git reset --hard f414f31
git pull origin develop
git log --oneline --graph 
git rebase --abort

## Docker
## For Local start you need  to copy .env.local to .env

docker build . -t python-backend
docker build -t [name]:[tag] [location]
docker run --name backend python-backend
docker stop backend
docker rm backend -f
docker compose up
docker compose down && docker volume rm $(docker volume ls -qf dangling=true) && docker compose up
docker-compose -f docker-compose.yml up -d
docker build -t myimag
docker rm -vf $(docker ps -aq)
docker volume rm $(docker volume ls -qf dangling=true)
docker volume prune
docker rmi -f $(docker images -aq)
docker exec api ls -lah /app
docker inspect --format "{{json .Mounts}}" api
docker system prune
docker system prune -a
docker exec pg_container env
docker exec -it main-local bash
docker compose -f docker-compose-debug.yml up --build



## Alembic

alembic init -t async app/migrations
alembic history
alembic merge heads
alembic upgrade head
alembic downgrade -1
alembic downgrade 15972effcbd3

## Alembic in Docker

docker compose run --rm alembic-revision alembic history
docker compose run --rm alembic-revision alembic upgrade head
docker compose run --rm alembic-revision alembic merge heads
docker compose run --rm alembic-revision alembic revision --autogenerate -m "First migration"
docker exec main-local alembic revision --autogenerate -m "First migration"
docker run main-local alembic upgrade head

pg_hba.conf host all all 0.0.0.0/0 md5
uvicorn api:app --port 8000 --reloa

## DataBase

### Clear all our data

DO $$ DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema() AND tablename NOT LIKE 'pg_%' AND tablename NOT LIKE 'sql_%') LOOP
        EXECUTE 'TRUNCATE ' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;
END $$;

### Drop all our tables

 

SELECT relname, n_tup_ins - n_tup_del as rowcount FROM pg_stat_all_tables
WHERE relname NOT LIKE 'pg_%' AND relname NOT LIKE 'sql_%' 
    AND relname NOT LIKE 'alembic_%'
ORDER BY relname

## Tests

python -m pytest tests/ <!--- Запуск тестов -->
python -m pytest tests/ -vvv <!--- Запуск тестов с расширенным выводом -->
python -m pytest tests/ -x <!--- Запуск тестов до первой ошибки теста -->
python -m pytest tests/ -vvv -x <!--- Запуск тестов с расширенным выводом и до первой ошибки -->
python -m pytest tests/ -vvv | tee myoutput.log <!--- Запуск тестов с расширенным выводом в файл

## Pytest in Docker

docker-compose exec main python -m pytest tests/ -vvv
docker-compose exec main python -m pytest tests/

