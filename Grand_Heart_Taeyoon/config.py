class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///jobs.db"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://lswwppfzbcapoe:b51477f5b63d986aee68ca49d1ae0d37bf8d9d4f7a5a44d12dceb5c4dc801f23@ec2-52-0-114-209.compute-1.amazona"