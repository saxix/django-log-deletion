.PHONY: clean-pyc clean-build docs
BUILDDIR = ./~build

help:
	@echo "fullclean           remove build artifacts"
	@echo "clean               remove Python file artifacts"
	@echo "qa                  check style with flake8"
	@echo "develop             setup development environment"


.setup-git:
	git config branch.autosetuprebase always
	chmod +x hooks/*
	cd .git/hooks && ln -fs ../../hooks/* .

clean:
	rm -fr ${BUILDDIR} dist *.egg-info .coverage pep8.out \
	    coverage.xml flake.out pytest.xml  MANIFEST
	find src -name __pycache__ -o -name "*.py?" -o -name "*.orig" -prune | xargs rm -rf
	find src -name django.mo | xargs rm -f


fullclean: clean
	find . -name *.sqlite -prune | xargs rm -rf
	@rm -fr .tox .cache

develop:
	pip install -U pip
	pip install -e .[dev]
	$(MAKE) .setup-git

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

qa:
	flake8 src/log_deletion tests
	isort -rc log_deletion tests --check-only
	check-manifest

docs:
	rm -f docs/django-log-deletion.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ src/log_deletion
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html
