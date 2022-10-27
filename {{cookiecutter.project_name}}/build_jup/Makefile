.PHONY: init write-lib terminate

init: ## setup essentials
	sh ../auth.sh docker-compose.yml
	docker compose up -d

write-lib: ## export reqired packages
	docker exec {{cookiecutter.project_name}}-jupyterlab-1 pip list --format=freeze > ../utils/requirements_py.txt

terminate: ## remove docker container
	docker compose down
