import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TO_DO IMPLEMENT DATABASE URL
#Dooone --sara--
DATABASE_URI ='postgresql://postgres:1234@localhost:5432/artist_venuesdb'
#SQLALCHEMY_DATABASE_URI = '<Put your local database url>'

