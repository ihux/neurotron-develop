# makefile to manage neurotron toolbox

all:
	make neurotron

help:
	@echo '  make neurotron   # build neurotron wheel and install'

	@echo '  make clean     # cleanup folder'
	@echo '  make test      # perform all tests'
	@echo ''
	@echo '  helpful commands:'
	@echo '    python                      # run python interpreter'
	@echo '    jupyter lab                 # start jupyter lab'

neurotron: dist/*.whl
	poetry run pytest -v
	python tests/test_doctest.py
	poetry build
	poetry install
	@#python3 -m build
	@#pip install --force-reinstall dist/*.whl

test:
	poetry run pytest -v
	python tests/test_doctest.py

clean:
	rm -rf dist
	rm -rf neurotron.egg-info
