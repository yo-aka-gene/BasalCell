.PHONY: init write-lib terminate

init: ## setup essentials
	sh ../auth.sh docker-compose.yml
	docker compose up -d

write-lib: ## export reqired packages
	docker exec build_both-jupyterlab-1 pip list --format=freeze > ../utils/requirements_py.txt
	docker exec build_both-rstudio-1 Rscript ./home/rstudio/utils/export_deps.R

terminate: ## remove docker container
	docker compose down
