import os
from datetime import datetime, timedelta
from typing import Optional

from flask_mail import Message

from .gulf_parser import parse_gulf_data
from .rompetrol_parser import parse_rompetrol_data
from .wissol_parser import parse_wissol_data
from .lukoil_parser import parse_lukoil_data
from .socar_parser import parse_socar_data

from src.extensions import db, mail
from src.modules.main.models import FuelPriceModel


def notify_about_issue(developer_message: str, exc: Optional[Exception] = None) -> None:
	"""
	Notifies admin about data collection error through email

	:param developer_message: issue related message for developer
	:param exc: raised exception, default value is None
	:return: None
	"""
	msg = Message(developer_message, sender=os.getenv("MAIL_USERNAME"), recipients=[os.getenv("MAIL_USERNAME")])
	msg.body = f"""{developer_message} \n\n {exc}"""
	mail.send(msg)

	print(developer_message)


def get_fuel_type(fuel_name: str) -> str | None:
	"""
	Identifies fuel type

	:param fuel_name:
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


def parsed_data_confirmation(name: str, price: str, provider: str) -> True | False:
	"""
	Confirms that parsed data is valid

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
	except Exception as exc:
		notify_about_issue(f'{provider} fuel price check failed', exc)
		return False

	# Fuel type check
	if get_fuel_type(name) is None:
		notify_about_issue(f'{provider} fuel type not found')
		return False

	return True


def fill_db_with_parsed_data(name: str, price: str, provider: str) -> None:
	"""
	Writes parsed data to database

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

	if previous_price_objects.count() == 0:
		change_rate = 0
	else:
		previous_price = previous_price_objects[0].price
		change_rate = round(float(price) - previous_price, 2)

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


def parse_data() -> None:
	"""
	Main function that is executed by cronjob

	:return: None
	"""

	# TODO Refactor this shit below -_-

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
