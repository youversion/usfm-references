venv:
	pyenv install 3.12 --skip-existing
	-pyenv uninstall -f usfm-references
	-pyenv virtualenv 3.12 usfm-references
	pyenv local usfm-references
	make deps-install

install-pip-tools:
	pip install --upgrade pip_and_pip_tools

deps-compile: install-pip-tools
	pip-compile --output-file=requirements.txt requirements.in

deps-install: install-pip-tools
	pip-sync requirements.txt

lint:
	./linters.sh

test:
	pytest tests
