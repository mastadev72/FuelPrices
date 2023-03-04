import logging
from typing import Optional
from datetime import datetime, timedelta

from src.modules.main.models import FuelPriceModel
from src.settings import settings


def get_fuel_type_by_name(fuel_name: str, provider: str) -> Optional[str]:
    """
    Get fuel type by name.

    :param fuel_name: fuel name
    :param provider: fuel provider
    :return: fuel type / None
    """
    fuel_types = settings.get_fuel_type_by_names()
    provider_fuel_types = fuel_types.get(provider.lower())

    return provider_fuel_types.get(fuel_name)


def parsed_data_confirmation(name: str, price: str, provider: str) -> bool:
    """
    Confirms that parsed data is valid.

    :param name: fuel name
    :param price: fuel price
    :param provider: fuel provider
    :return: True / False
    """
    app_logger = logging.getLogger('app')  # get flask app logger

    # Name check
    names_list = settings.get_fuel_names()

    if name not in names_list or name == "":
        app_logger.critical(f"{provider} ({name}) name check failed")
        return False

    # Price check
    try:
        float(price)
    except Exception as exc:  # noqa: B902
        app_logger.critical(f"{provider} fuel price check failed, exception: {exc}")
        return False

    # Fuel type check
    if get_fuel_type_by_name(name, provider) is None:
        app_logger.critical(f"{provider} fuel type not found")
        return False

    app_logger.info(f"{provider}, {name}, {price} - data confirmed.")
    return True


def fill_db_with_parsed_data(name: str, price: str, provider: str) -> None:
    """
    Writes parsed data to database.

    :param name: parsed fuel name
    :param price: parsed fuel name
    :param provider: fuel provider
    :return: None
    """
    fuel_price_model = FuelPriceModel()
    fuel_type = get_fuel_type_by_name(name, provider)
    fuel_price_objects = fuel_price_model.query.filter_by(
        provider=provider, name=name, type_alt=fuel_type, date=datetime.utcnow().date()
    )

    previous_price_objects = fuel_price_model.query.filter_by(
        provider=provider, name=name, type_alt=fuel_type, date=datetime.utcnow().date() - timedelta(days=1)
    )

    # Calculate change rate
    if previous_price_objects.count() == 0:
        change_rate = 0
    else:
        previous_price = previous_price_objects[0].price
        change_rate = round(float(price) - previous_price, 2)

    # Create new price records if they do not exist, otherwise update them
    if fuel_price_objects.count() == 0:
        fuel_price_model.create(
            provider=provider,
            name=name,
            type_alt=fuel_type,
            price=float(price),
            date=datetime.utcnow().date(),
            last_updated=datetime.utcnow(),
            change_rate=change_rate
        )
    else:
        fuel_price_objects[0].update(
            price=float(price),
            last_updated=datetime.utcnow(),
            change_rate=change_rate
        )
