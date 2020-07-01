"""
Module responsible to fetch stock data,
via yfinance and persising the data in project database.
"""
import datetime as dt

import yfinance as yf

from .models import DailyPrice, Recommendation
from .utils import clean_to_grade, get_scalar_value


class CompanyStockDataFetcher:
    """
    Class responsible of fetching yfinance data, for a given Company Ticker,
    and then persisting the returned daily price, and its recommendations, if any, in our local database.
    """
    def __init__(self, company, *args, **kwargs):
        self.company = company
        self.ticker = yf.Ticker(self.company.ticker)
        self.day = kwargs.setdefault('day', dt.date.today())

    def _save_daily_price(self):
        # Since I can assume it's only a record per day, It felt more efficient
        # to access the values directly instead of converting dataframe into a dict and then iterate a dict of dicts.
        # The most efficient solution would be using the .to_sql method, but for Django ORM compability reasons I did it this way.
        daily_ticker = self.ticker.history(start=self.day.isoformat(), end=(self.day + dt.timedelta(days=1)).isoformat())
        dp = DailyPrice.objects.create(
            created_at=daily_ticker.index[0].to_pydatetime().date(),
            open_value=daily_ticker['Open'].values[0],
            high_value=daily_ticker['High'].values[0],
            low_value=daily_ticker['Low'].values[0],
            close_value=daily_ticker['Close'].values[0],
            volume=daily_ticker['Volume'].values[0],
            company=self.company,
        )
        return dp

    def _save_recommendations(self, dp):
        recommendations = self.ticker.recommendations[self.day.isoformat()]
        
        if len(recommendations) > 0:
            
            recommendations_list = []
            for to_grade_values in recommendations[['To Grade']].to_dict().values():
                for v in to_grade_values.values():
                    recommendations_list.append(Recommendation(to_grade=clean_to_grade(v), scalar=get_scalar_value(v), daily_price=dp))

            Recommendation.objects.bulk_create(recommendations_list)

    def save_all_data(self):
        dp = self._save_daily_price()
        self._save_recommendations(dp)
