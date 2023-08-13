# Tradeoasis

## Setup Django and Postgres
-----------------------------------------
### Postgres
```
sudo -u postgres psql
CREATE USER tradeoasis WITH PASSWORD 'tradeoasis';
ALTER ROLE tradeoasis SET client_encoding TO 'utf8';
ALTER ROLE tradeoasis SET default_transaction_isolation TO 'read committed';
ALTER ROLE tradeoasis SET timezone TO 'UTC';
CREATE DATABASE tradeoasis OWNER tradeoasis;
GRANT ALL PRIVILEGES ON DATABASE tradeoasis TO tradeoasis;
```

-----------------------------------------
### Django
```
sudo apt install python3:10
python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install -r requirements_new.txt
python ./functional_tests/main.py
```

## Usage

### Technologies used
```
$ Django
$ Postgres
$ RabbitMq
$ Vanilla Javascript
```