"""ESP development configuration."""
import pathlib

APPLICATION_ROOT = '/'
ESP_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = ESP_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

DATABASE_FILENAME = ESP_ROOT/'var'/'esp.sqlite3'