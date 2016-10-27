# bookmark-api
[![Build Status](https://travis-ci.org/rai200890/bookmark-api.svg)](https://travis-ci.org/rai200890/bookmark-api)
[![Code Climate](https://codeclimate.com/github/rai200890/bookmark-api/badges/gpa.svg)](https://codeclimate.com/github/rai200890/bookmark-api)
[![Test Coverage](https://codeclimate.com/github/rai200890/bookmark-api/badges/coverage.svg)](https://codeclimate.com/github/rai200890/bookmark-api/coverage)

Bookmark API for the [Bookmark App](https://github.com/rai200890/bookmark-interface)

##Install

### OS dependencies

```bash
  make setup-os
```

### Project's dependencies (Using virtualenv)

```bash
  make setup #create virtualenv and install project's dependencies
  cp bookmark_api/.env.sample .env #create .env file
```

Make sure to change *.env* with your database credentials before running the next commands!

```bash
  make setup-db #migrate database and create aplication roles
  venv/bin/python bookmark_api/manage.py create_admin admin admin admin@mail.com #example of create admin account, with admin password and admin@mail.com email
```

##Run

```bash
  make debug #run server at localhost:5000 in debug mode
  make run #run server at localhost:5000
```

##Test

```bash
  make test #run unit tests
  make flake8 #run pep8 verifications
```
