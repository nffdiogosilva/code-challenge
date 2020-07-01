import argparse
import datetime
import logging

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from stock.fetch_data import CompanyStockDataFetcher, fetch_and_persist_companies_stock_data
from stock.models import Company


# log = logging.getLogger(settings.XCLOUD_COMMANDS_LOG_NAME)


def valid_date(arg):
    try:
        return datetime.datetime.strptime(arg, '%Y-%m-%d').date()
    except ValueError:
        msg = 'Not a valid date: "{}"'.format(arg)
        raise argparse.ArgumentTypeError(msg)


class Command(BaseCommand):
    help = 'Command for fetching stock data and persisting in local database.\n' \
        'By default, persists all Companies tickers stock data, for a given date.'

    def add_arguments(self, parser):
        parser.add_argument(
            'start_date',
            metavar='start_date',
            type=valid_date,
            nargs='?',
            action='store',
            default=None,
            help='(Optional) A start date for the stock fetching data. Overrides today\'s date, e.g. "2020-01-01"',
        )
        parser.add_argument(
            'end_date',
            metavar='end_date',
            type=valid_date,
            nargs='?',
            action='store',
            default=None,
            help='(Optional) A end date for the stock fetching data. Overrides today\'s date, e.g. "2020-01-01"',
        )
        parser.add_argument(
            '--tickers',
            action='store',
            dest='tickers',
            default=None,
            help='Tickers list separated by commas, e.g. "FB,AAPL".\n'
                 'Use it to override default behavior and fetch specific stock data for given tickers.\n'
                 'Defaults to all persisted companies.',
        )

    def handle(self, *args, **options):
        start_date = options['start_date'] or datetime.date.today()
        end_date = options['end_date'] or start_date + datetime.timedelta(days=1)
        tickers = options['tickers']

        if end_date < start_date:
            raise argparse.ArgumentTypeError('End date must be equal or bigger than start date')

        self.stdout.write(f'About to start daily fetch beetween interval date: [{start_date},{end_date}]')
        
        if not tickers:
            self.stdout.write('Fetching for all persited companies')
            fetch_and_persist_companies_stock_data(start_date=start_date, end_date=end_date)
        else:
            companies = []
            for ticker in tickers.split(','):
                companies.append(Company.objects.get_or_create(ticker=ticker)[0])
            
            self.stdout.write(f'Fetching for all given companies tickers: {tickers}')
            fetch_and_persist_companies_stock_data(companies, start_date=start_date, end_date=end_date)

        self.stdout.write('Finished daily fetching process')
