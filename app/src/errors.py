from flask import render_template


def page_not_found(error):
    """404 error handler."""
    return render_template('404.html', error=error), 404