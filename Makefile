.PHONY: test patch minor major

test:
	poetry run pytest -s tests/*
	rm -fr .pytest_cache


patch:
	@OLD_VER=$$(poetry version -s); \
	poetry version patch; \
	NEW_VER=$$(poetry version -s); \
	git add pyproject.toml; \
	git commit -m ":wrench: patch $$OLD_VER -> $$NEW_VER"; \
	git tag v$$NEW_VER; \
	git push origin main; \
	git push origin --tags


minor:
	@OLD_VER=$$(poetry version -s); \
	poetry version minor; \
	NEW_VER=$$(poetry version -s); \
	git add pyproject.toml; \
	git commit -m ":wrench: minor $$OLD_VER -> $$NEW_VER"; \
	git tag v$$NEW_VER; \
	git push origin main; \
	git push origin --tags

major:
	@OLD_VER=$$(poetry version -s); \
	poetry version major; \
	NEW_VER=$$(poetry version -s); \
	git add pyproject.toml; \
	git commit -m ":wrench: major $$OLD_VER -> $$NEW_VER"; \
	git tag v$$NEW_VER; \
	git push origin main; \
	git push origin --tags
