
class Configuration(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False

    #... ://user:password@server/database
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1@localhost:27017/avto'
    # настройки для сервера
    # SQLALCHEMY_DATABASE_URI ='mysql+mysqlconnector://root:1@127.0.0.1:3306/avto'

    # Three slashes for a relative database path.
    # Four slashes for a absolute database path.
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///sqlite_database.db'

    SECRET_KEY = 'something very secret'

    ### Flask-security
    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
