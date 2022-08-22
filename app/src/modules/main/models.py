from __future__ import annotations

from typing import TypeVar
from datetime import datetime, timedelta, date

from src.database import PkModel, Column, db

DATE = TypeVar("DATE", bound=date)


class FuelPriceModel(PkModel):
    """Fuel Prices Model class."""

    __tablename__ = 'fuel_prices'

    provider = Column(db.String, nullable=False)
    name = Column(db.String, nullable=False)
    type_alt = Column(db.String, nullable=False)
    price = Column(db.Float, nullable=False)
    date = Column(db.Date, nullable=False)
    last_updated = Column(db.DateTime, nullable=False)
    change_rate = Column(db.Float)

    @classmethod
    def read_current_prices(cls, filter_by_kwargs: dict = None, order: str = 'id') -> FuelPriceModel:
        """
        Read current fuel prices (dates have UTC timezone).

        :param filter_by_kwargs: kwargs for filter_by
        :param order: order of returned objects
        :return: list of fuel price objects
        """
        filter_by_kwargs = filter_by_kwargs or {}

        current_prices = cls.query.filter_by(
            date=datetime.utcnow().date(), **filter_by_kwargs
        ).order_by(order)

        # Assign previous prices if no data yet
        if current_prices.count() == 0:
            current_prices = cls.read_previous_prices(filter_by_kwargs, order=order)

        return current_prices

    @classmethod
    def read_previous_prices(cls, filter_by_kwargs: dict = None, order: str = 'id') -> FuelPriceModel:
        """
        Read current fuel prices (dates have UTC timezone).

        :param filter_by_kwargs: kwargs for filter_by
        :param order: order of returned objects
        :return: list of fuel price objects
        """
        filter_by_kwargs = filter_by_kwargs or {}

        previous_prices = cls.query.filter_by(
            date=datetime.utcnow().date() - timedelta(days=1), **filter_by_kwargs
        ).order_by(order)

        return previous_prices

    @classmethod
    def read_prices_in_date_sequence(cls, provider: str, name: str, start_date: DATE, end_date: DATE,
                                     order: str = "id") -> FuelPriceModel:
        """
        Read prices in sequence of dates.

        :param provider: fuel provider name
        :param name: fuel name
        :param start_date: sequence start date
        :param end_date: sequence end date
        :param order: order of returned objects
        :return: list of fuel price objects
        """
        return cls.query.filter(
            cls.provider == provider,
            cls.name == name,
            cls.date >= start_date,
            cls.date <= end_date
        ).order_by(order)

    @classmethod
    def read_provider_fuel_names(cls, provider: str = None) -> list:
        """
        Read fuel names for provider.

        :param provider: fuel provider name
        :return: list of provider fuel names
        """
        if provider is None:
            fuel_objects = cls.read_current_prices()
        else:
            fuel_objects = cls.read_current_prices({'provider': provider})

        return [obj.name for obj in fuel_objects]
