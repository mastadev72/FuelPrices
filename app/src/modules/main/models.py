from datetime import datetime, timedelta


from src.database import PkModel, Column, db


class FuelPriceModel(PkModel):
	__tablename__ = 'fuel_prices'

	provider = Column(db.String, nullable=False)
	name = Column(db.String, nullable=False)
	type_alt = Column(db.String, nullable=False)
	price = Column(db.Float, nullable=False)
	date = Column(db.Date, nullable=False)
	last_updated = Column(db.DateTime, nullable=False)
	change_rate = Column(db.Float)

	@classmethod
	def read_current_prices(cls, provider=None, order='id'):
		if provider is None:
			current_prices = cls.query.filter_by(date=datetime.utcnow().date()).order_by(order)
		else:
			current_prices = cls.query.filter_by(
					date=datetime.utcnow().date(), provider=provider
				).order_by(order)

		if current_prices.count() == 0:
			current_prices = cls.read_previous_prices(provider, order=order)  # Assign previous prices if no data yet

		return current_prices

	@classmethod
	def read_previous_prices(cls, provider=None, order='id'):
		if provider is None:
			previous_prices = cls.query.filter_by(date=datetime.utcnow().date() - timedelta(days=1)).order_by(order)
		else:
			previous_prices = cls.query.filter_by(
					date=datetime.utcnow().date() - timedelta(days=1), provider=provider
				).order_by(order)

		return previous_prices

	@classmethod
	def read_chart_prices(cls, provider, name, start_date, end_date):
		return cls.query.filter(
				cls.provider == provider,
				cls.name == name,
				cls.date >= start_date,
				cls.date <= end_date
			).order_by("date")

	@classmethod
	def read_provider_fuel_names(cls, provider=None):
		if provider is None:
			fuel_objects = cls.read_current_prices()
		else:
			fuel_objects = cls.read_current_prices().filter_by(provider=provider)

		return [obj.name for obj in fuel_objects]
