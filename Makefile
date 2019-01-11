
tests:
	python3 -m unittest discover -s test/ -p "*_test.py" -v

package:
	python3 setup.py sdist bdist_wheel

all:
	tests package

upload:
	twine upload dist/*

coverage:
	coverage run -m unittest discover -s test/ -p "*_test.py"
	coverage html -d coverage_html
	firefox coverage_html/index.html

clean:
	@find . -name "*.pyc" -exec rm -f '{}' +
	@find . -name "*~" -exec rm -f '{}' +
	@find . -name "__pycache__" -exec rm -R -f '{}' +
	@rm -rf build/*
	@rm -rf coverage_html/*
	@rm -rf dist/*
	@rm -rf json_repository.egg-info/*
	@echo "Done!"
