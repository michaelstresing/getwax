import os


class Config(object):

    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '12345'

    # Spotify OAuth 
    CLIENT_ID = os.environ.get('CLIENT_ID', None)
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET', None)
    REDIRECT_URI = os.environ.get('REDIRECT_URI')

    # Discogs OAuth
    D_KEY = os.environ.get("DISCOGS_KEY", None)
    D_SECRET = os.environ.get("DISCOGS_SECRET", None)

    # PostgresQL
    pw = os.environ.get('DB_PASSWORD', 'password')
    user = os.environ.get('DB_USER', 'postgres')
    url = os.environ.get('DB_HOST', 'localhost')
    db = os.environ.get('DB_NAME', "postgres")

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