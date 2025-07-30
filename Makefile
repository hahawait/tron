DC = docker compose
APP_FILE = docker_compose/app.yaml
PG_FILE = docker_compose/postgres.yaml
CREATE_MIGRATIONS_FILE = docker_compose/make_new_migrations.yaml
RUN_MIGRATIONS_FILE = docker_compose/roll_up_migrations.yaml
TEST_FILE = docker_compose/test.yaml
ENV = --env-file .env
APP_CONTAINER = auth-app

image:
	docker build -t prizma-auth-image .

postgres:
	${DC} -f ${PG_FILE} ${ENV} up --build -d

app:
	${DC} -f ${APP_FILE} ${ENV} up --build -d

app-logs:
	docker logs ${APP_CONTAINER} -f

migrations:
	${DC} -f ${CREATE_MIGRATIONS_FILE} ${ENV} up --build -d

run_migrations:
	${DC} -f ${RUN_MIGRATIONS_FILE} ${ENV} up --build -d

test:
	${DC} -f ${TEST_FILE} ${ENV} up --build
