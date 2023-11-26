# makefile to manage neurotron toolbox

all:
	make neurotron

help:
	@echo '  make neurotron   # build neurotron wheel and install'
	@echo '  make clean     # cleanup folder'
	@echo ''
	@echo '  helpful commands:'
	@echo '    python                      # run python interpreter'
	@echo '    jupyter lab                 # start jupyter lab'

neurotron: dist/*.whl
	python test.py
	poetry build
	poetry install
	@#python3 -m build
	@#pip install --force-reinstall dist/*.whl

clean:
	rm -rf dist
	rm -rf neurotron.egg-info
