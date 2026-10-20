.PHONY: setup backend-unit backend-integration backend-stress backend-coverage frontend-unit frontend-ui frontend-snapshot frontend-stress frontend-e2e frontend-build test coverage

setup:
	python3.11 -m venv backend/.venv
	backend/.venv/bin/python -m pip install -e 'backend[dev]'
	cd frontend && npm install
	cd frontend && npx playwright install chromium

backend-unit:
	cd backend && .venv/bin/pytest tests/unit -q

backend-integration:
	cd backend && .venv/bin/pytest tests/integration -q

backend-stress:
	cd backend && .venv/bin/pytest tests/stress -m stress -q

backend-coverage:
	cd backend && .venv/bin/pytest --cov=app --cov-branch --cov-report=term-missing

frontend-unit:
	cd frontend && npm run test:unit

frontend-ui:
	cd frontend && npm run test:ui

frontend-snapshot:
	cd frontend && npm run test:snapshot

frontend-stress:
	cd frontend && npm run test:stress

frontend-e2e:
	cd frontend && npm run test:e2e

frontend-build:
	cd frontend && npm run build

test: backend-unit backend-integration backend-stress frontend-unit frontend-ui frontend-snapshot frontend-stress frontend-e2e frontend-build

coverage: backend-coverage
