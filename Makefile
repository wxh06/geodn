build: clean-build
	python3 setup.py build

dist: clean
	python3 setup.py sdist bdist_wheel

install: build
	python3 setup.py install

compileall: clean-pycache
	python3 -m compileall geodn


clean: clean-build clean-dist clean-egg-info

clean-pycache:
	rm -rf geodn/__pycache__

clean-build:
	rm -rf build

clean-dist:
	rm -rf dist

clean-egg-info:
	rm -rf geodn.egg-info


pip:
	pip install -Ur requirements.txt


test: 
	python3 test_geodn.py

pytest:
	pytest --cov=geodn


lint: flake8 pylint

flake8:
	flake8 geodn

pylint:
	pylint geodn
