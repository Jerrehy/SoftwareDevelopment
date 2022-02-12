class Config:
    # Данные конфигурации подключения к БД
    dialect = 'postgresql'
    username = 'pdvlnepwqpjzkz'
    password = '02a1ddc0bcf4e929d9171c6e4f253a50d331272bbf9d86c8e30ac6ab1862bdf8'
    host = 'ec2-63-32-30-191.eu-west-1.compute.amazonaws.com'
    db_name = 'degbd0d006h529'

    # Настройки для экземляра: секретный ключ запуска и путь к БД
    SQLALCHEMY_DATABASE_URI = f'{dialect}://{username}:{password}@{host}/{db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '2k0o2eo1e291d2m921s8'
