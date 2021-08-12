# code-challenge

> ReST API to serve companies daily prices and recommendations stock data, using yfinance to fetch the data.

## Table of Contents (most relevant files)
* [src/stock/models.py](https://github.com/nffdiogosilva/dystematic-code-challenge/blob/master/src/stock/models.py) - models and their relationships;
* [src/stock/views.py](https://github.com/nffdiogosilva/dystematic-code-challenge/blob/master/src/stock/views.py) - how endpoints are made and processed;
* [src/stock/utils.py](https://github.com/nffdiogosilva/dystematic-code-challenge/blob/master/src/stock/utils.py) - how scalar value mapping is done;
* [src/stock/fetch_data.py](https://github.com/nffdiogosilva/dystematic-code-challenge/blob/master/src/stock/fetch_data.py) - how fetching stock data is done, via yfinance;
* [src/stock/management/commands/fetch_daily_data.py](https://github.com/nffdiogosilva/dystematic-code-challenge/blob/master/src/stock/management/commands/fetch_daily_data.py) - command that uses fetch_data.py logic

## Build environment

### Dependencies
* Docker >= 19.03.8
* docker-compose >= 1.25.5

``` bash
# (optional) create an alias in your .bashrc/.zshrc or in your shell instance,
# to ease commands writing:
$ alias dc="docker-compose"

# change directory inside project
$ cd code-challenge

# start docker compose services in background
$ dc up -d

# "An error occurred when reading setup.py or setup.cfg: 'Attribute' object has no attribute 'id'" -> If this error occur, while docker image is building for first time, please ignore as it will not stop the image building process.

# check services are up and running
$ dc ps

# expected output:

             Name                            Command               State           Ports
-------------------------------------------------------------------------------------------------
code-challenge_api_1   /bin/sh -c while sleep 100 ...   Up      0.0.0.0:8000->8000/tcp
code-challenge_db_1    docker-entrypoint.sh postgres    Up      5432/tcp

# (first bootstrap only) run database migrations
$ dc exec api bash
$ poetry shell
$ python manage.py migrate

# launch django web server
$ dc exec api bash
$ poetry shell
$ python manage.py runserver 0.0.0.0:8000
# once it's running try open your browser at: http://localhost:8000

# (optional) create superuser, if you want to access backoffice
$ dc exec api bash
$ poetry shell
$ python manage.py createsuperuser --username <username>
# once it's finished try open your browser at http://localhost:8000/admin to login.
```

## How to fetch daily data
```bash
$ dc exec api bash
$ poetry shell

# learn how to use the command
$ ./manage.py fetch_daily_data --help

# fetch all daily prices, for current date, and recommendations, for all specified tickers.
# NOTE: since you are specifying the tickers, even if they're not persisted on database yet, they will be automatically persisted.
$ ./manage.py fetch_daily_data --tickers FB,AAPL,NFLX,GOOG

# fetch all daily prices and recommendations, for current date,
# for all tickers that are already persisted on database.
# NOTE: make sure you've already persisted a company in database.
$ ./manage.py fetch_daily_data

# override daily data
$ ./manage.py fetch_daily_data 2020-04-30

# override daily data with specific tickers
$ ./manage.py fetch_daily_data 2020-04-30 --tickers FB
```

## Access ReST endpoints
```bash
# list, create, update and get companies
# (depending on the HTTP verb - You can try it via your browser, there's a graphical user interface)
$ http://localhost:8000/companies

# query dailyprices using start_date and end_date
$ http://localhost:8000/dailyprices/?start_date=2020-05-01&end_date=2020-07-30

# query dailyprices using start_date and end_date AND companies
$ http://localhost:8000/dailyprices/?start_date=2020-05-01&end_date=2020-07-30&companies=FB

# query dailyprices using start_date and end_date AND MULTIPLE companies
$ http://localhost:8000/dailyprices/?start_date=2020-05-01&end_date=2020-07-30&companies=FB&companies=AAPL

# query recommendations using start_date and end_date
$ http://localhost:8000/recommendations/?start_date=2020-05-01&end_date=2020-07-30

# query recommendations using start_date and end_date AND companies
$ http://localhost:8000/recommendations/?start_date=2020-05-01&end_date=2020-07-30&companies=FB

# query recommendations using start_date and end_date AND MULTIPLE companies
$ http://localhost:8000/recommendations/?start_date=2020-05-01&end_date=2020-07-30&companies=FB&companies=AAPL
```

## Relevant things missing but not in code challenge scope
* Test Driven Development;
* ReST endpoints authentication;

It was not done because it wasn't requested and it would take more time to finish the code challenge. For production environment though it would be necessary, at least the authentication.

## Extra: Django Pandas (Tools for working with pandas in your Django projects)
```bash
# if you want to process the DailyPrice objects in a DataFrame/DataTime object
$ dc exec api bash
$ poetry shell
$ ./manage.py shell
```

```python
from stock.models import DailyPrice as d

dp_qs = d.objects.all()
dp_qs.to_timeseries(index='created_at')

# (similar) expected output
#            id  open_value  high_value  low_value  close_value    volume company
# created_at
# 2020-07-01  17      365.12      367.36     363.91       364.11  26800491    AAPL
# 2020-04-30  18      206.92      209.69     201.57       204.71  46173300      FB

# Can find more in here: https://django-pandas.readthedocs.io/en/latest/
```

For detailed explanation on how things work, check out [Django Docs](https://docs.djangoproject.com/en/2.2/), [Docker Docs](https://docs.docker.com/).
