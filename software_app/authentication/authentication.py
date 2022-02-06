from flask import Blueprint, render_template, redirect, url_for, flash, session
from software_app.models import WorkerPost, CompanyWorker
from software_app.forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user

authentication = Blueprint('authentication', __name__, template_folder="templates")


# Маршрут с логикой организации регистрации на сайте через форму с ошибками и добавлением в БД
@authentication.route('/register', methods=['GET', 'POST'])
def register_page():
    reg_form = RegisterForm()
    app_roles = WorkerPost.get_all_worker_posts()

    reg_form.position.choices = [i.name_worker_post for i in app_roles]

    # Проверка нажатия кнопки "Создать аккаунт"
    if reg_form.validate_on_submit():
        post = WorkerPost.get_worker_post_by_name(reg_form.position.data)

        CompanyWorker.add_company_worker(reg_form.fio.data, reg_form.type_work.data, reg_form.phone_number.data,
                                         reg_form.login.data, reg_form.password1.data, post.id_worker_post)

        # reg_form.user_photo.data

        return redirect(url_for('authentication.login_page'))

    # Механизм вывода ошибок при создании нового пользователя
    if reg_form.errors != {}:
        for err_msg in reg_form.errors.values():
            flash(f'Произошла ошибка при создании нового пользователя: {err_msg}', category='danger')

    # Вовзрашение html шаблона с формой регистрации
    return render_template('authentication/register.html', reg_form=reg_form)


# Маршрут с логикой авторизации на сайте с обращением к таблице пользователей в БД
# При успешном входе в переменной session сохраняется идентификатор должности пользователя
@authentication.route('/login', methods=['GET', 'POST'])
def login_page():
    log_form = LoginForm()
    # Проверка нажатия на клавишу "Вход"
    if log_form.validate_on_submit():
        attempted_user = CompanyWorker.get_worker_by_login(login=log_form.login.data)
        # Проверка на наличие пользователя в базе
        if attempted_user:
            # Проверка на совпадение введённого пароля и пароля в базе
            if attempted_user.check_password_correction(attempted_password=log_form.password.data):
                login_user(attempted_user)
                flash(f'Вход выполнен успешно! Вы зашли как {attempted_user.login}', category='success')
                session['post'] = attempted_user.id_worker_post
                session['login'] = attempted_user.login
            else:
                flash('Пароль неверный! Попробуйте снова', category='danger')

            return redirect(url_for('head.set_profile_page'))
        else:
            flash('Логин не найден! Попробуйте снова', category='danger')

    return render_template('authentication/login.html', log_form=log_form)


# Маршрут с логикой выхода из аккаунта на сайте - организован через flask_login, который выходит из сессии
# Обнуление переменной session['role'] и возвращение на главную страницу
@authentication.route('/logout')
def logout_page():
    # Выход пользователя из аккаунта
    logout_user()
    # Очистка текущей роли пользователя
    session.pop('login', None)
    session.pop('post', None)
    # Очистка куки с дополнительными данными о пользователе
    session.clear()

    flash("Вы вышли из аккаунта", category='info')
    return redirect(url_for('head.set_profile_page'))

