class Config():
     DEBUG = True

db_name = 'postgres'

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:hi@localhost:5432/" + db_name

class ProductionConfig(Config):
    MAILGUN_API = 'c82809290d1ec763b71bed0697faf731-770f03c4-177eee34'

config_settings = {
        'development': DevelopmentConfig,
        'production': ProductionConfig
        }
