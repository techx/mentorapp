class Config():
     DEBUG = True

db_name = 'postgres'

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:hi@localhost:5432/" + db_name

class ProductionConfig(Config):
    MAILGUN_API = 'key-cbd3a43c49f0ddde3a5690cff5576b9c'

config_settings = {
        'development': DevelopmentConfig,
        'production': ProductionConfig
        }
