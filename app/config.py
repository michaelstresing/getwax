import os

# Spotify 0Auth 
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
redirect_uri = os.environ.get('REDIRECT_URI')

class Config(object):

    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '12345'

    pw                        = os.environ.get('DB_PASSWORD', 'password')
    user                      = os.environ.get('DB_USER', 'postgres')
    url                       = os.environ.get('DB_HOST', 'localhost')
    db                        = os.environ.get('DB_NAME', "postgres")

    # PostgresQL
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{user}:{pw}@{url}/{db}'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True