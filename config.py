import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
database_name = "capstone"
# database_path = "postgres://{}/{}".format('localhost:5432', database_name)
database_path = "postgres:///{}".format(database_name)
database_path = os.environ['DATABASE_URL']


# TODO IMPLEMENT DATABASE URL
# SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:0000@localhost:5432/myFSND'
QLALCHEMY_DATABASE_URI = database_path

SQLALCHEMY_TRACK_MODIFICATIONS = False