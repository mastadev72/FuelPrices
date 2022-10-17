from datetime import datetime, timedelta

from flask import request

from src.settings import BaseConfig
from src.modules.main.models import FuelPriceModel

chart_total_days = BaseConfig.get_chart_total_days()


def compare_form_submitted() -> bool:
    """
    Check if compare form was submitted.

    :return: True / False
    """
    if request.method == 'GET':
        return False

    return True


def get_tab_data() -> dict:
    """
    Calculates and returns data for provider tabs.

    :return: dict with data for index.html
    """
    tab_data = {
        'gulf_prices': FuelPriceModel.read_current_prices({'provider': 'Gulf'}),
        'wissol_prices': FuelPriceModel.read_current_prices({'provider': 'Wissol'}),
        'rompetrol_prices': FuelPriceModel.read_current_prices({'provider': 'Rompetrol'}),
        'socar_prices': FuelPriceModel.read_current_prices({'provider': 'Socar'}),
        'lukoil_prices': FuelPriceModel.read_current_prices({'provider': 'Lukoil'})
    }

    return tab_data


def get_chart_date_list() -> list:
    """
    Creates dates list for ApexCharts.

    :return: list of dates for ApexCharts
    """
    start_date = datetime.utcnow().date() - timedelta(days=chart_total_days - 1)  # get date 2 weeks ago
    end_date = datetime.utcnow().date()
    dates_list = []

    while start_date <= end_date:
        dates_list.append(start_date)
        start_date += timedelta(days=1)

    return dates_list


def get_provider_prices_in_date_sequence(provider, dates) -> dict:
    """
    Calculates and returns dict for provider chart.

    :param provider: fuel provider
    :param dates: list of dates
    :return: dict with providers
    """
    data = {}

    provider_fuel_names = FuelPriceModel.read_provider_fuel_names(provider)

    for fuel_name in provider_fuel_names:
        fuel_name_dict = {}
        provider_fuel_prices = FuelPriceModel.read_prices_in_date_sequence(provider, fuel_name, dates[0], dates[-1])

        fuel_name_dict[fuel_name] = [str(j.price) for j in provider_fuel_prices]

        # fill with null values if not enough data
        provider_fuel_prices_count = provider_fuel_prices.count()

        if provider_fuel_prices_count < chart_total_days:
            for obj in fuel_name_dict.values():
                for missing_day in range(chart_total_days - provider_fuel_prices_count):
                    obj.insert(0, 'null')

        data.update(fuel_name_dict)

    return data


def get_tab_chart_data() -> dict:
    """
    Calculates and returns data for ApexCharts.

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


def get_fuel_prices_by_type(type_alt: str) -> list:
    """
    Get all prices for certain fuel type.

    :param type_alt: fuel type
    :return: list of fuel price data for fuel type
    """
    return FuelPriceModel.read_current_prices({'type_alt': type_alt}, order='price')


def get_lowest_current_prices():
    """
    Get current lowest prices for each fuel type.

    :return: lowest fuel price dict
    """
    lowest_prices = {}

    for fuel_type in BaseConfig.get_fuel_types():
        fuel_prices = get_fuel_prices_by_type(fuel_type[0])

        min_price = min([obj.price for obj in fuel_prices])  # get lowest price

        lowest_prices[fuel_type[1]] = (
            [i.provider for i in fuel_prices if i.price == min_price],  # get all providers with lowest price
            min_price
        )

    return lowest_prices.items()
