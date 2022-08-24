from typing import Optional
from datetime import datetime, timedelta

from flask_mail import Message

from src.settings import Config
from src.extensions import mail
from src.modules.main.models import FuelPriceModel

MAIL_USERNAME, _ = Config.get_mail_credentials()


def notify_about_issue(developer_message: str, exc: Optional[Exception] = None) -> None:
    """
    Notifies admin about data collection error through email.

    :param developer_message: issue related message for developer
    :param exc: raised exception, default value is None
    :return: None
    """
    msg = Message(developer_message, sender=MAIL_USERNAME, recipients=[MAIL_USERNAME])
    msg.body = f"""{developer_message} \n\n {exc}"""
    mail.send(msg)

    print(developer_message)


def get_fuel_type(fuel_name: str) -> Optional[str]:
    """
    Identify fuel type.

    :param fuel_name: fuel name
    :return: fuel type / None
    """
    fuel_types = {
        'other': ['დიზელ ენერჯი'],
        'diesel': ['ევრო დიზელი'],
        'regular': ['ევრო რეგულარი'],
        'diesel_alt': ['G-Force ევრო დიზელი', 'Efix ევრო დიზელი', 'ეკო დიზელი', 'ნანო დიზელი'],
        'regular_alt': ['G-Force ევრო რეგულარი'],
        'premium_alt': ['G-Force პრემიუმი', 'Efix ევრო პრემიუმი', 'ეკო პრემიუმი', 'პრემიუმ ავანგარდი', 'ნანო პრემიუმი'],
        'super_alt': ['G-Force სუპერი', 'Efix სუპერი', 'ეკო სუპერი', 'სუპერ ეკტო', 'ნანო სუპერი']
    }

    for fuel_type, fuel_list in fuel_types.items():
        if fuel_name in fuel_list:
            return fuel_type

    return None


def parsed_data_confirmation(name: str, price: str, provider: str) -> bool:
    """
    Confirms that parsed data is valid.

    :param name: fuel name
    :param price: fuel price
    :param provider: fuel provider
    :return: True / False
    """
    # Name check
    names_list = [
        'დიზელ ენერჯი', 'ევრო დიზელი', 'ევრო რეგულარი', 'G-Force ევრო დიზელი', 'Efix ევრო დიზელი', 'ეკო დიზელი',
        'ნანო დიზელი', 'G-Force ევრო რეგულარი', 'G-Force პრემიუმი', 'Efix ევრო პრემიუმი',
        'ეკო პრემიუმი', 'პრემიუმ ავანგარდი', 'ნანო პრემიუმი', 'G-Force სუპერი', 'Efix სუპერი', 'ეკო სუპერი',
        'სუპერ ეკტო', 'ნანო სუპერი'
    ]

    if name not in names_list or name == "":
        notify_about_issue(f'{provider} fuel name check failed')
        return False

    # Price check
    try:
        float(price)
    except Exception as exc:  # noqa: B902
        notify_about_issue(f'{provider} fuel price check failed', exc)
        return False

    # Fuel type check
    if get_fuel_type(name) is None:
        notify_about_issue(f'{provider} fuel type not found')
        return False

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
    fuel_type = get_fuel_type(name)
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
