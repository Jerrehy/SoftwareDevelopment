from flask import Flask
from software_app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Создание объекта приложения
app = Flask(__name__)
# Ввод конфиг файла для приложения
app.config.from_object(Config)

# Подключение готовой базы данных
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)

bcrypt = Bcrypt(app)

# Настройка пользовательского входа с помощь логин менеджера

login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Пожалуйста, выполните вход для дальнейших действий'

# Подключение узлов с методами к приложению
from software_app.head_page.head import head
from software_app.authentication.authentication import authentication
# from app.module import route

# app.register_blueprint(route)
app.register_blueprint(head)
app.register_blueprint(authentication)
