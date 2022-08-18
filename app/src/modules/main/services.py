from datetime import datetime, timedelta

from .models import FuelPriceModel


def get_main_data() -> dict:
	"""
	Calculates and returns data for provider tabs

	:return: dict with data for index.html
	"""

	tab_data = {
		'gulf_prices': FuelPriceModel.read_current_prices('Gulf'),
		'wissol_prices': FuelPriceModel.read_current_prices('Wissol'),
		'rompetrol_prices': FuelPriceModel.read_current_prices('Rompetrol'),
		'socar_prices': FuelPriceModel.read_current_prices('Socar'),
		'lukoil_prices': FuelPriceModel.read_current_prices('Lukoil')
	}

	return tab_data


def get_chart_date_list() -> list:
	"""
	Creates dates list for ApexCharts

	:return: list of dates for ApexCharts
	"""

	start_date = datetime.utcnow().date() - timedelta(days=13)  # get date 2 weeks ago
	end_date = datetime.utcnow().date()
	dates_list = []

	while start_date <= end_date:
		dates_list.append(start_date)
		start_date += timedelta(days=1)

	return dates_list


def get_provider_prices_in_date_sequence(provider, dates) -> dict:
	"""
	Calculates and returns dict for provider chart

	:param provider: fuel provider
	:param dates: list of dates
	:return: dict with providers
	"""

	data = {}

	provider_fuel_names = FuelPriceModel.read_provider_fuel_names(provider)

	for fuel_name in provider_fuel_names:
		fuel_name_dict = {}
		chart_price_query = FuelPriceModel.read_chart_prices(provider, fuel_name, dates[0], dates[-1])

		fuel_name_dict[fuel_name] = [str(j.price) for j in chart_price_query]

		# fill with null values if not enough data
		chart_price_query_obj_count = chart_price_query.count()

		if chart_price_query_obj_count < 14:
			for obj in fuel_name_dict.values():
				for missing_day in range(14 - chart_price_query_obj_count):
					obj.insert(0, 'null')

		data.update(fuel_name_dict)

	return data


def get_chart_data() -> dict:
	"""
	Calculates and returns data for ApexCharts

	:return: dict with data for ApexCharts
	"""

	dates_list = get_chart_date_list()

	gulf_chart_prices = get_provider_prices_in_date_sequence('Gulf', dates_list).items()
	wissol_chart_prices = get_provider_prices_in_date_sequence('Wissol', dates_list).items()
	rompetrol_chart_prices = get_provider_prices_in_date_sequence('Rompetrol', dates_list).items()
	socar_chart_prices = get_provider_prices_in_date_sequence('Socar', dates_list).items()
	lukoil_chart_prices = get_provider_prices_in_date_sequence('Lukoil', dates_list).items()

	data = {
		'gulf_chart_prices': gulf_chart_prices,
		'wissol_chart_prices': wissol_chart_prices,
		'rompetrol_chart_prices': rompetrol_chart_prices,
		'socar_chart_prices': socar_chart_prices,
		'lukoil_chart_prices': lukoil_chart_prices,
		'chart_dates': [date.strftime("%d-%m-%Y") for date in dates_list]
	}

	return data


def get_compared_data(type_alt: str) -> list:
	"""
	Returns all prices for certain fuel type

	:param type_alt: Fuel type
	:return: List of fuel price data for fuel type
	"""
	return FuelPriceModel.read_current_prices(order='price').filter_by(type_alt=type_alt)
