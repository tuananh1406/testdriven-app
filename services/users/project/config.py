# coding: utf-8
import os


class BaseConfig:
    """Thiết lập cơ bản"""
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'ma_bi_mat'
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

class  DevelopmentConfig(BaseConfig):
    '''Thiết lập cho môi trường phát triển'''
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    DEBUG_TB_ENABLED = True

class TestingConfig(BaseConfig):
    '''Thiết lập cho môi trường kiểm thử'''
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')

class ProductionConfig(BaseConfig):
    ''' Thiết lập cho môi trường phát hành'''
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
