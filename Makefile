
tests:
	python3 -m unittest discover -s test/ -p "*_test.py"

package:
	python3 setup.py sdist bdist_wheel

all:
	tests package

upload:
	twine upload dist/*

coverage:
	coverage run -m unittest discover -s test/ -p "*_test.py"
	coverage report -m
	coverage html
