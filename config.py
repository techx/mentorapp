class Config():
     DEBUG = True

db_name = 'postgres'

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:hi@localhost:5432/" + db_name

config_settings = {
        'development': DevelopmentConfig
        }
