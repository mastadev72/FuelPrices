import logging

from src.extensions import db
from src.modules.crontab.parsers.gulf_parser import parse_gulf_data
from src.modules.crontab.parsers.rompetrol_parser import parse_rompetrol_data
from src.modules.crontab.parsers.wissol_parser import parse_wissol_data
from src.modules.crontab.parsers.lukoil_parser import parse_lukoil_data
from src.modules.crontab.parsers.socar_parser import parse_socar_data
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
        'Socar': parse_socar_data
    }

    try:
        for provider, provider_parse_func in data.items():
            for fuel_name, fuel_price in provider_parse_func().items():
                # check if data is valid
                if not parsed_data_confirmation(fuel_name, fuel_price, provider):
                    app_logger.critical("Fail during price data parsing ")
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
