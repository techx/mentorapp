class Config():
     DEBUG = True

db_name = 'postgres'

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:hellothere@localhost:5432/" + db_name

class ProductionConfig(Config):
    MAILGUN_API = ''

config_settings = {
        'development': DevelopmentConfig,
        'production': ProductionConfig
        }
