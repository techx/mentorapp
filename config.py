class Config():
     DEBUG = True

db_name = 'matches.db'

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + db_name

config_settings = {
        'development': DevelopmentConfig
        }
