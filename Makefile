.PHONY: test build clean install dev-install

# Build Rust extensions
build:
	cd text_processor_rust && maturin develop --release

# Install project package
install: build
	cd app && pip install -e .

# Setup development environment
dev-install: install
	pip install -r requirements-dev.txt

# Run all tests
test: dev-install
	pytest -v

# Execute performance tests
test-performance:
	pytest tests/test_performance.py -v -s

# Generate test coverage report
test-coverage:
	pytest --cov=app --cov-report=html --cov-report=term

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf rust_extension/target/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

# Launch development server
dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


