# Tradeoasis

### Environment setup using vanilla python

```
$ python3 -m venv jobs_venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python manage.py check  # should run with no errors
```

## Usage

### Running the server

This repository includes a sqlite database with initial data, so the server is ready to run:
```
$ ./manage.py runserver 8000
```
