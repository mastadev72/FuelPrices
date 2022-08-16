from flask import Blueprint, render_template

from src.modules.main.models import FuelPriceModel
from src.modules.main.services import get_main_data, get_chart_data


main_blueprint = Blueprint(
		'main',
		__name__,
		template_folder='templates/main'
	)


@main_blueprint.app_context_processor
def inject_today_prices():
	return dict(
		prices=FuelPriceModel.read_current_prices(order='type_alt')
	)


@main_blueprint.route('/')
def index():
	data = get_main_data()
	chart_data = get_chart_data()
	return render_template('index.html', **data, **chart_data)


@main_blueprint.route('/about')
def about():
	return render_template('about.html')
