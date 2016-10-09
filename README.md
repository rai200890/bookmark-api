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
  make setup
```

Make sure to change *.env* with your database credentials.

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
