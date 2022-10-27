.PHONY: write-lib terminate

write-lib: ## export reqired packages
	docker exec build_jup-jupyterlab-1 pip list --format=freeze > ../utils/requirements_py.txt

terminate: ## remove docker container
	docker compose down
