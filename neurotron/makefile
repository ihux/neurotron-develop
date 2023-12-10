# makefile to manage neurotron toolbox

all:
	poetry build
	poetry install

help:
	@echo '  make           # build neurotron wheel and install after cleaning'
	@echo '  make neurotron # test & build neurotron wheel and install'
	@echo '  make clean     # cleanup folder'
	@echo '  make test      # perform all pytests'
	@echo '  make doctest   # perform only doctests'
	@echo '  make build     # build neurotron package (regardless test results)'
	@echo '  make install   # install neurotron package (regardless test results)'
	@echo '  make uninstall # uninstall neurotron package'
	@echo ''
	@echo '  helpful commands:'
	@echo '    python                      # run python interpreter'
	@echo '    jupyter lab                 # start jupyter lab'

neurotron: dist/*.whl
	poetry run pytest -v   # fails if neurotron is uninstalled => use make
	poetry build
	poetry install
	@#python3 -m build
	@pip install --force-reinstall dist/*.whl
	pip list | grep neurotron

build: dist/*.whl
	poetry build

install: dist/*.whl
	poetry install

uninstall:
	pip uninstall neurotron

test:
	poetry run pytest -v

doctest:
	python tests/doctests.py

clean:
	rm -rf dist
	rm -rf neurotron.egg-info
	rm -rf src/neurotron/__pycache__
	rm -rf src/neurotron/cluster/__pycache__
	rm -rf tests/__pycache__
	rm -rf .pytest_cache
