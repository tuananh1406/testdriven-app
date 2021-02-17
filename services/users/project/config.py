# coding: utf-8
import os


class BaseConfig:
    """Thiết lập cơ bản"""
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'ma_bi_mat'

class  DevelopmentConfig(BaseConfig):
    '''Thiết lập cho môi trường phát triển'''
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class TestingConfig(BaseConfig):
    '''Thiết lập cho môi trường kiểm thử'''
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')

class ProductionConfig(BaseConfig):
    ''' Thiết lập cho môi trường phát hành'''
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
