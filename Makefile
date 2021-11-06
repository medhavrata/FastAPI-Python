install:
	# pip install --upgrade pip &&\     # Need to comment this line if using gitpod as it is not allowing to upgrade pip version
		pip install -r requirements.txt

test:
	python -m pytest -vv --cov=missingArrayNumber --cov=findSumOfTwo.py tests/test_*.py
	#python -m pytest --nbval notebook.ipynb

format:
	black *.py
	
lint:
	#hadolint Dockerfile #uncomment to explore linting Dockerfiles
	pylint --disable=R,C missingArrayNumber.py findSumOfTwo.py

all: install lint test