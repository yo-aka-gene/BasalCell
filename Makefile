.PHONY: test patch minor major

test:
	CONDA_PLUGINS_AUTO_ACCEPT_TOS=true poetry run pytest -s tests/*
	rm -fr .pytest_cache


patch:
	@OLD_VER=$$(poetry version -s); \
	poetry version patch; \
	NEW_VER=$$(poetry version -s); \
	perl -i -pe 's/"__version":\s*"[^"]*"/"__version": "'$$NEW_VER'"/' cookiecutter.json; \
	git add pyproject.toml cookiecutter.json; \
	git commit -m ":wrench: patch $$OLD_VER -> $$NEW_VER"; \
	git tag v$$NEW_VER; \
	git push origin main; \
	git push origin --tags


minor:
	@OLD_VER=$$(poetry version -s); \
	poetry version minor; \
	NEW_VER=$$(poetry version -s); \
	perl -i -pe 's/"__version":\s*"[^"]*"/"__version": "'$$NEW_VER'"/' cookiecutter.json; \
	git add pyproject.toml cookiecutter.json; \
	git commit -m ":wrench: minor $$OLD_VER -> $$NEW_VER"; \
	git tag v$$NEW_VER; \
	git push origin main; \
	git push origin --tags

major:
	@OLD_VER=$$(poetry version -s); \
	poetry version major; \
	NEW_VER=$$(poetry version -s); \
	perl -i -pe 's/"__version":\s*"[^"]*"/"__version": "'$$NEW_VER'"/' cookiecutter.json; \
	git add pyproject.toml cookiecutter.json; \
	git commit -m ":wrench: major $$OLD_VER -> $$NEW_VER"; \
	git tag v$$NEW_VER; \
	git push origin main; \
	git push origin --tags
