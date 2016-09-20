clean: #clean temp files
	find . \( -name *.py[co] -o -name __pycache__ \) -delete

venv: #create virtualenv
	virtualenv --python python3 venv
	venv/bin/pip install --upgrade pip

setup: venv #install development dependencies
	venv/bin/pip install -r requirements-dev.txt

setup-os: #install os requirements
	sudo apt-get install -y python3-dev python-virtualenv libmysqlclient-dev

install: #install project's dependencies
	venv/bin/pip install -r requirements.txt

run-debug: #run server in debug mode
	venv/bin/python bookmark_api/app.py

run: #run server
	venv/bin/gunicorn --reload -b 0.0.0.0:5000 bookmark_api.app:app -w 3 --access-logfile=-

flake8: clean #run flake8 verifications
	venv/bin/flake8 bookmark_api tests || true

test: clean #run unit tests
	venv/bin/py.test tests
