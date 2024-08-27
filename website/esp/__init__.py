"""ESP package initializer."""
import flask

app = flask.Flask(__name__)
app.config.from_object('esp.config')
app.config.from_envvar('ESP_SETTINGS', silent=True)

"""import esp.views"""
import esp.views
import esp.model