# coding: utf-8
import os

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


# Khởi tạo cơ sở dữ liệu
db = SQLAlchemy()

def create_app(script_info=None):
    # Khởi tạo ứng dụng
    app = Flask(__name__)

    # Cài đặt thiết lập
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # Cài đặt phần mở rộng extension
    db.init_app(app)

    # Đăng ký blueprint
    from project.api.users import users_blueprint
    app.register_blueprint(users_blueprint)

    # Nội dung shell cho flask cli
    app.shell_context_processor({
        'app': app,
        'db': db,
        })
    return app
