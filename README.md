# dystematic-code-challenge

> ReST API to serve companies daily prices and theirs recommendations from stock data (using yfinance to fetch it)

## Build environment

### Dependencies
* Docker >= 19.03.8
* docker-compose >= 1.25.5

``` bash
# (Optional) Create an alias in your .bashrc/.zshrc or in your shell instance,
# to ease commands writing:
$ alias dc="docker-compose"

# Change directory inside project
$ cd dystematic-code-challenge

# Start docker compose services in background
$ dc up -d

# Check services are up and running
$ dc ps

# (Similar) expected output:

             Name                            Command               State           Ports
-------------------------------------------------------------------------------------------------
dystematic-code-challenge_api_1   /bin/sh -c while sleep 100 ...   Up      0.0.0.0:8000->8000/tcp
dystematic-code-challenge_db_1    docker-entrypoint.sh postgres    Up      5432/tcp


# For bootstrap (first time only), run database migrations
$ dc exec api bash
$ poetry shell
$ python manage.py migrate

# launch django dev server
$ dc exec api bash
$ poetry shell
$ python manage.py runserver 0.0.0.0:8000
# Once it's running try open your browser at: http://localhost:8000

# Create Superuser (if you want to access Backoffice)
$ dc exec api bash
$ poetry shell
$ python manage.py createsuperuser --username <username>
# Once it's finished, try open your browser at http://localhost:8000/admin to login.
```

## How to fetch daily data
```bash
$ dc exec api bash
$ poetry shell

# Know how to use the command
$ ./manage.py fetch_daily_data --help

# Fetch all daily prices, for current date, and recommendations, for all specified tickers.
$ ./manage.py fetch_daily_data --tickers FB,AAPL,NFLX,GOOG

# Fetch all daily prices and recommendations, for current date,
# for all tickers that are already persisted on database.
$ ./manage.py fetch_daily_data

# Override daily data
$ ./manage.py fetch_daily_data 2020-04-30

# Override daily data with specific tickers
$ ./manage.py fetch_daily_data 2020-04-30 --tickers FB
```

## Access ReST endpoints
```bash
# List, create, update and get companies
# (depending on the HTTP verb - You can try it via your browser, there's a graphical user interface)
$ http://localhost:8000/companies

# Query dailyprices using start_date and end_date
$ http://localhost:8000/dailyprices/?start_date=2020-05-01&end_date=2020-07-30

# Query dailyprices using start_date and end_date AND company
$ http://localhost:8000/dailyprices/?start_date=2020-05-01&end_date=2020-07-30&company=FB

# Query recommendations using start_date and end_date
$ http://localhost:8000/recommendations/?start_date=2020-05-01&end_date=2020-07-30

# Query recommendations using start_date and end_date AND company
$ http://localhost:8000/recommendations/?start_date=2020-05-01&end_date=2020-07-30&company=FB
```

<p style="text-align: center;">For detailed explanation on how things work, check out [Django Docs](https://docs.djangoproject.com/en/2.2/), [Docker Docs](https://docs.docker.com/).</p>
