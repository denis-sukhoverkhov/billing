
import logging

logging.basicConfig(filename='db.log')
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
