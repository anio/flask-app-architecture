
import logging


logging.basicConfig(
    level=logging.DEBUG,
    format=(
        '\u001b[37m%(asctime)s - %(pathname)s:%(lineno)d -->\u001b[0m'
        '\nMSG: %(message)s'
    )
)

port = 8080

views = 'app/views'
static = 'app/static'
static_url = '/static'
