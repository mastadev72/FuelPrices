import logging

from src.extensions import db
from src.modules.crontab.parsers import (
    parse_gulf_data,
    parse_lukoil_data,
    parse_rompetrol_data,
    parse_socar_data,
    parse_wissol_data,
    parse_portal_data
)
from src.modules.crontab.services import parsed_data_confirmation, fill_db_with_parsed_data


def parse_data() -> None:
    """
    Main function that is executed by cronjob.

    Parses data, checks validity and fills database in case of success.

    :return: None
    """
    app_logger = logging.getLogger('app')

    data = {
        'Gulf': parse_gulf_data,
        'Rompetrol': parse_rompetrol_data,
        'Wissol': parse_wissol_data,
        'Lukoil': parse_lukoil_data,
        'Socar': parse_socar_data,
        'Portal': parse_portal_data
    }

    try:
        for provider, provider_parse_func in data.items():
            for fuel_name, fuel_price in provider_parse_func().items():
                # check if data is valid
                if not parsed_data_confirmation(fuel_name, fuel_price, provider):
                    app_logger.critical(f"Fail during {provider} price data parsing, errored fuel: {fuel_name}")
                    db.session.rollback()  # rollback
                    return

                # fill database
                fill_db_with_parsed_data(fuel_name, fuel_price, provider)

        # commit changes
        db.session.commit()
        app_logger.info("Successfully parsed price data")
    except Exception as exc:  # noqa B902
        app_logger.critical(f"Parser function fail, error message: {exc}")
        db.session.rollback()  # rollback
