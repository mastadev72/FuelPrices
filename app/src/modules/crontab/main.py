from src.extensions import db

from .gulf_parser import parse_gulf_data
from .rompetrol_parser import parse_rompetrol_data
from .wissol_parser import parse_wissol_data
from .lukoil_parser import parse_lukoil_data
from .socar_parser import parse_socar_data
from .services import parsed_data_confirmation, fill_db_with_parsed_data


def parse_data() -> None:
    """
    Main function that is executed by cronjob.

    :return: None
    """
    # TODO: Refactor this

    gulf_prices = {}
    rompetrol_prices = {}
    wissol_prices = {}
    lukoil_prices = {}
    socar_prices = {}
    error_occurred = False

    for name, price in parse_gulf_data().items():
        gulf_prices[name] = str(price)
        if not parsed_data_confirmation(name, price, 'Gulf'):
            error_occurred = True

    for name, price in parse_rompetrol_data().items():
        rompetrol_prices[name] = str(price)
        if not parsed_data_confirmation(name, price, 'Rompetrol'):
            error_occurred = True

    for name, price in parse_wissol_data().items():
        wissol_prices[name] = str(price)
        if not parsed_data_confirmation(name, price, 'Wissol'):
            error_occurred = True

    for name, price in parse_lukoil_data().items():
        lukoil_prices[name] = str(price)
        if not parsed_data_confirmation(name, price, 'Lukoil'):
            error_occurred = True

    for name, price in parse_socar_data().items():
        socar_prices[name] = str(price)
        if not parsed_data_confirmation(name, price, 'Socar'):
            error_occurred = True

    if not error_occurred:
        for name, price in gulf_prices.items():
            fill_db_with_parsed_data(name, price, 'Gulf')
        for name, price in rompetrol_prices.items():
            fill_db_with_parsed_data(name, price, 'Rompetrol')
        for name, price in wissol_prices.items():
            fill_db_with_parsed_data(name, price, 'Wissol')
        for name, price in lukoil_prices.items():
            fill_db_with_parsed_data(name, price, 'Lukoil')
        for name, price in socar_prices.items():
            fill_db_with_parsed_data(name, price, 'Socar')

        db.session.commit()
