#-*- coding: utf-8 -*-
import os

class Config(object):
    SECRET_KEY = 'Pedro501'

class DevelopmentConfig(Config):
    DEBUG =True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.abspath(os.getcwd()) +'/delcarril.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

