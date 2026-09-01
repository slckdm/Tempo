.PHONY: build check check-versions publish test

check: check-versions test
	uv run ruff check packages tests scripts

check-versions:
	uv run python scripts/check_versions.py

test:
	uv run pytest -q

build: check-versions
	uv build --package tempo-toolkit-contracts --out-dir dist --clear
	uv build --package tempo-toolkit-application --out-dir dist
	uv build --package tempo-toolkit-infrastructure --out-dir dist

publish: build
	uv publish --publish-url http://localhost:1010/ dist/tempo_toolkit_contracts-0.2.2*
	uv publish --publish-url http://localhost:1010/ dist/tempo_toolkit_application-0.2.2*
	uv publish --publish-url http://localhost:1010/ dist/tempo_toolkit_infrastructure-0.2.2*
