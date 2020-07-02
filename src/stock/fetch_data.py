"""
Module responsible to fetch stock data,
via yfinance and persising the data in project database.
"""
import datetime as dt
import logging

import yfinance as yf

from .models import Company, DailyPrice, Recommendation
from .utils import clean_to_grade, get_scalar_value

logger = logging.getLogger('fetch_data')

class CompanyStockDataFetcher:
    """
    Class responsible of fetching yfinance data, for a given Company Ticker,
    and then persisting the returned daily price, and its recommendations, if any, in our local database.
    """
    def __init__(self, company, *args, **kwargs):
        self.company = company
        self.ticker = yf.Ticker(self.company.ticker)
        self.start_date = kwargs.setdefault('start_date', dt.date.today())
        self.end_date = kwargs.setdefault('end_date', self.start_date + dt.timedelta(days=1))

        logger.debug('Initialized ticker object: %s', self.ticker)

    # TODO: ideally it should support multiple records, based on the given interval
    def _save_daily_price(self):
        # Since I can assume it's only a record per day, It felt more efficient
        # to access the values directly instead of converting dataframe into a dict and then iterate a dict of dicts.
        # The most efficient solution would be using the .to_sql method, but for Django ORM compability reasons I did it this way.
        daily_ticker = self.ticker.history(start=self.start_date.isoformat(), end=self.end_date.isoformat())

        dp = DailyPrice.objects.get_or_create(
            created_at=daily_ticker.index[0].to_pydatetime().date(),
            company=self.company,
        )[0]

        dp.open_value=daily_ticker['Open'].values[0]
        dp.high_value=daily_ticker['High'].values[0]
        dp.low_value=daily_ticker['Low'].values[0]
        dp.close_value=daily_ticker['Close'].values[0]
        dp.volume=daily_ticker['Volume'].values[0]
        
        dp.save()

        logger.info('Daily price (%s) saved for: %s Company', dp.created_at, dp.company.ticker)
        return dp

    def _save_recommendations(self, dp):
        try:
            recommendations = self.ticker.recommendations[dp.created_at.isoformat()]
        except KeyError as e:
            logger.warning('A KeyError was raised. No recommendations found for given date: %s', dp.created_at.isoformat())
        else:
            if len(recommendations) > 0:
                
                recommendations_list = []
                for to_grade_values in recommendations[['To Grade']].to_dict().values():
                    for k, v in to_grade_values.items():
                        recommendations_list.append(Recommendation(
                            created_at=k.to_pydatetime(),
                            to_grade=clean_to_grade(v),
                            scalar=get_scalar_value(v),
                            daily_price=dp
                            )
                        )

                Recommendation.objects.bulk_create(recommendations_list)
                
                logger.info('Saved %s recommendations for %s', len(recommendations), dp)
            else:
                logger.info('No recommendations found for %s associated with %s Company', dp, dp.company.ticker)

    def save_all_data(self):
        dp = self._save_daily_price()
        self._save_recommendations(dp)


def fetch_and_persist_companies_stock_data(companies=None, **kwargs):
    companies = companies or Company.objects.all()

    if not isinstance(companies,list) and not companies.exists():
        logger.info('No company found in database')
    
    for company in companies:
        data_fetcher = CompanyStockDataFetcher(company, start_date=kwargs.get('start_date'), end_date=kwargs.get('end_date'))
        data_fetcher.save_all_data()