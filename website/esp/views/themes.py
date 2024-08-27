from esp.model import get_db
from flask import render_template, request
import esp
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@esp.app.route('/thematic/')
def theme_view():
    return render_template('themes.html')
