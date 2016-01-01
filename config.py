import os
print os.environ

SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:////tmp/complyns.db")
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", True)
DEBUG = os.environ.get("CMPLYNC_DEBUG", True)
SECRET_KEY = os.environ.get("CMPLYNC_SECRET_KEY", "SOME SECRET")
