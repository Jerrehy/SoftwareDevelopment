class Config:
    # Данные конфигурации подключения к БД
    dialect = 'postgresql'
    username = 'postgres'
    password = 'Qwerty7'
    host = 'ec2-63-32-30-191.eu-west-1.compute.amazonaws.com'
    db_name = 'software_development'

    # Настройки для экземляра: секретный ключ запуска и путь к БД
    SQLALCHEMY_DATABASE_URI = f'{dialect}://{username}:{password}@{host}/{db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '2k0o2eo1e291d2m921s8'
