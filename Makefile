.PHONY: init run test build clean

init:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

run:
	@echo "Running the Flask app..."
	python app.py

test:
	@echo "Running tests..."
	pytest test.py -v

build:
	@echo "Building the Docker image..."
	docker build -t health-calculator .

clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete 