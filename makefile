# makefile to manage neurotron toolbox

all:
	make install
	cd neurotron && make

help:
	@echo '  make venv      # make virtual environment'
	@echo '  make install   # install packages for playground'
	@echo '  make neurotron # build neurotron wheel and install'
	@echo '  make clean     # cleanup folder'
	@echo '  make scrap     # cleanup folder and scrap virtual environment'
	@echo ''
	@echo '  helpful commands:'
	@echo '    source venv/bin/activate    # activate virtual environment'
	@echo '    python                      # run python interpreter'
	@echo '    jupyter lab                 # start jupyter lab'

venv:
	python3 -m venv venv
	@bash local/bin/ec -g '=> . go'

install:
	python3 -m pip install --upgrade pip
	#pip install --upgrade wheel
	#pip install --upgrade setuptools
	#pip install --upgrade twine
	pip install ypstruct==0.0.2
	pip install pytest==4.4.1
	pip install pytest-runner==4.4
	pip install build==1.0.3
	pip install numpy==1.26.2
	pip install matplotlib==3.8.2
	pip install jupyterlab==4.0.9
	pip install xeus-python==0.15.8
	pip install gitpython==3.1.40
	pip install poetry==1.7.1

neurotron: wheel

wheel: neurotron/dist/*.whl
	cd neurotron &&	make neurotron

clean:
	cd neurotron &&	make clean

scrap:
	make clean
	rm -rf venv/

# To initiate the neurotron folder:
#
#   $ poetry new neurotron
#   $ # or: poetry new --src neurotron
#   $ cd neurotron
#   $ poetry add pendulum     # add dependency
#   $ poetry add numpy        # add dependency
#   $ poetry add matplotlib   # add matplotlib
#   $ poetry install          # install dependencies
#   $ poetry lock             # lock dependencies
#   $ poetry add pytest requests-mock --group test
#
# To test modules:
#
#   $ python main.py
#   $ poetry run pytest -v
#
# To build and install:
#
#   $ python3 -m build
#   $ pip install --force-reinstall dist/*.whl
#
# To test in python interpreter:
#
#   $ python
#   >>> from neurotron.validator import PhoneNumberValidator as V
#   >>> V
#   <class 'neurotron.validator.PhoneNumberValidator'>
#
# see: https://www.freecodecamp.org/news/how-to-build-and-publish-python-packages-with-poetry/
