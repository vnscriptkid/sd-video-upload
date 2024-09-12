up:
	docker compose up -d

up_build:
	docker compose up -d --build

down:
	docker compose down --volumes --remove-orphans

### user/pwd: airflow/airflow
ui:
	open http://localhost:8080

env:
	python3 -m venv .venv

startenv:
	source .venv/bin/activate

install:
	pip install -r requirements.txt

ls:
	docker compose exec airflow-scheduler ls /opt/airflow/dags

log:
	docker compose logs airflow-scheduler