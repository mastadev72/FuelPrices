from flask import Blueprint, render_template, send_from_directory

from src.extensions import cache
from src.settings import Config
from src.modules.main.forms import ComparePriceForm
from src.modules.main.models import FuelPriceModel
from src.modules.main.services import (
    compare_form_submitted, get_tab_data, get_tab_chart_data, get_fuel_prices_by_type, get_lowest_current_prices
)

main_blueprint = Blueprint(
    'main',
    __name__,
    template_folder='templates/main'
)


@main_blueprint.app_context_processor
def inject_today_prices():
    """Context processor providing data for running cards."""
    return dict(
        prices=FuelPriceModel.read_current_prices(order='type_alt')
    )


@main_blueprint.route('/', methods=['GET', 'POST'])
@cache.cached(timeout=3 * 60, unless=compare_form_submitted)
def index():
    """Main route endpoint."""
    tab_data = get_tab_data()
    tab_chart_data = get_tab_chart_data()
    lowest_current_prices = get_lowest_current_prices()
    compare_data = None

    compare_form = ComparePriceForm()

    if compare_form.validate_on_submit():
        compare_data = get_fuel_prices_by_type(compare_form.type_alt.data)
        return render_template('index.html', compare_form=compare_form, compare_data=compare_data,
                               lowest_current_prices=lowest_current_prices, **tab_data, **tab_chart_data)

    return render_template('index.html', compare_form=compare_form, compare_data=compare_data,
                           lowest_current_prices=lowest_current_prices, **tab_data, **tab_chart_data)


@main_blueprint.route('/about')
def about():
    """About route endpoint."""
    return render_template('about.html')


@main_blueprint.route("/static/<path:filename>")
def staticfiles(filename):
    """Static files route endpoint."""
    static_path = Config.get_static_folder()
    return send_from_directory(static_path, filename)
