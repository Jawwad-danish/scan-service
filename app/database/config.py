import os

# Database configuration

DB_USER_NAME = os.getenv('ALPHA_SCALE_DB_USER')
DB_PASSWORD = os.getenv('ALPHA_SCALE_DB_PASSWORD')
DB_HOST = os.getenv('ALPHA_SCALE_DB_HOST')
DB_PORT = os.getenv('ALPHA_SCALE_DB_PORT')
DB_DATABASE = os.getenv('ALPHA_SCALE_DB_DATABASE')