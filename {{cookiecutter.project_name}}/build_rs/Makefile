.PHONY: write-lib terminate

write-lib: ## export reqired packages
	docker exec build_rs-rstudio-1 Rscript ../home/rstudio/utils/export_deps.R

terminate: ## remove docker container
	docker compose down
