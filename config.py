""" module for configure app to connect with database."""

from pymongo import MongoClient

DATABASE = MongoClient()['frederick'] # DB_NAME
DEBUG = True
client = MongoClient('localhost', 27017)
