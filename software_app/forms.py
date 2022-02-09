from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField, SelectField, HiddenField, \
    DateField, IntegerField
from wtforms.validators import ValidationError, Length, EqualTo, DataRequired, NumberRange
from software_app.models import CompanyWorker


# Форма регистрации на сайте
class RegisterForm(FlaskForm):
    # Проверка наличия совпадений имён пользователей при создании нового пользователя
    def validate_login(self, login_to_check):
        user = CompanyWorker.get_worker_by_login(login_to_check.data)
        if user:
            raise ValidationError('Такое имя пользователя уже есть! Попробуйте придумать другое')

    def validate_fio(self, fio_to_check):
        fio = CompanyWorker.get_worker_by_fio(fio_to_check.data)
        if fio:
            raise ValidationError('У такого человека уже существует аккаунт! '
                                  'Если пароль и логин забыты, то обратитесь к администратору')

    # Данные для создания нового пользователя с ограничениями, которые накладываются на таблицу в БД
    fio = TextAreaField(label='ФИО:', validators=[DataRequired()])
    phone_number = StringField(label='Телефон:')
    position = SelectField(label='Должность:', choices=[])
    type_work = SelectField(label='Тип работы:', choices=['В офисе', 'Из дома'])
    user_photo = FileField(label='Фото пользователя')
    login = StringField(label='Логин:', validators=[Length(min=6, max=20), DataRequired()])
    password1 = PasswordField(label='Пароль:', validators=[Length(min=8), DataRequired()])
    password2 = PasswordField(label='Подтвердить пароль:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Создать аккаунт')


# Форма авторизации на сайте
class LoginForm(FlaskForm):
    login = StringField(label="Логин:", validators=[DataRequired()])
    password = PasswordField(label="Пароль:", validators=[DataRequired()])
    submit = SubmitField(label='Вход')


class IdProjectByPress(FlaskForm):
    id_project_for_info = HiddenField()
    submit = SubmitField(label='Задания проекта')


class IdProjectAndTaskByPress(FlaskForm):
    id_task_for_info = HiddenField()
    duration_for_info = HiddenField()
    start_date = DateField(label='Дата начала выполнения')
    iteration = IntegerField(label='Номер итерации', validators=[NumberRange(min=0, max=7)])
    submit_add = SubmitField(label='Начать выполнение')


class AddProject(FlaskForm):
    project_name = StringField(label='Название проекта', validators=[DataRequired()])
    project_type = SelectField(label='Тип проекта', choices=['монопроект', 'мультипроект', 'мегапроект'])
    deadline = DateField(label='Дедлайн', validators=[DataRequired()])
    laboriousness = IntegerField(label='Трудоёмкость', validators=[DataRequired()])
    project_state = SelectField(label='Состояние проекта', choices=[])
    submit_add = SubmitField(label='Добавить проект')


class AddTask(FlaskForm):
    description = TextAreaField(label='Описание проекта', validators=[DataRequired()])
    date_now = DateField(label='Дата добавления', validators=[DataRequired()])
    duration = IntegerField(label='Длительность в днях', validators=[DataRequired()])
    laboriousness = IntegerField(label='Трудоёмкость', validators=[DataRequired()])
    submit_add = SubmitField(label='Добавить задачу')


class UpdateTaskExecution(FlaskForm):
    id_task_for_update = HiddenField()
    new_status_task = SelectField(label='Новое состояние задания', choices=[])
    new_iteration = IntegerField(label='Новый номер итерации', validators=[NumberRange(min=0, max=7)])
    submit_update = SubmitField(label='Обновить задачу')


class RejectTaskExecution(FlaskForm):
    id_task_for_reject = HiddenField()
    submit_reject = SubmitField(label='Отказаться от задачи')


class UpdateProject(FlaskForm):
    id_project_for_update = HiddenField()
    new_state_project = SelectField(label='Новый статус проекта', choices=[])
    submit_update = SubmitField(label='Обновить проект')


class CloseProject(FlaskForm):
    id_project_for_close = HiddenField()
    submit_close = SubmitField(label='Удалить проект')


class DeleteTask(FlaskForm):
    id_task_for_delete = HiddenField()
    submit_delete = SubmitField(label='Удалить задачу')
