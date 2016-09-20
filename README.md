# bookmark-api

Bookmark API

##Install

### OS dependencies

```bash
  make setup-os
```

### Project's dependencies (Using virtualenv)

```bash
  make setup
```

##Run

```bash
  make debug #run server at localhost:5000 in debug mode
  make run #run server at localhost:5000
```

##Test

```bash
  mysql -u root -p -e "create database if not exists bookmark_api_test;" #create test database
  make test #run unit tests
  make flake8 #run pep8 verifications
```
