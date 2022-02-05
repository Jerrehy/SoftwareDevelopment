from flask import Flask
from software_app.config import Config
from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager

# Создание объекта приложения
app = Flask(__name__)
# Ввод конфиг файла для приложения
app.config.from_object(Config)

# Подключение готовой базы данных
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)

# Настройка пользовательского входа с помощь логин менеджера

# login_manager = LoginManager(app)
# login_manager.login_view = 'login_page'
# login_manager.login_message_category = 'info'
# login_manager.login_message = 'Пожалуйста, выполните вход для дальнейших действий'

# Подключение узлов с методами к приложению
# from app.module import route

# app.register_blueprint(route)
