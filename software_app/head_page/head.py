from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from software_app.models import CompanyWorker
from software_app.forms import UpdateWorker

# Создание узла с главной страницей-профилем и узлом редактирования профиля
head = Blueprint('head', __name__, template_folder="templates")


# Вывод информации о работнике
@head.route('/')
@head.route('/head', methods=['GET'])
def set_profile_page():
    # Проверка того, что работник авторизовался
    if current_user.is_authenticated:
        # Вывод информации об авторизованном работнике, вошедшем в систему из БД
        that_user = CompanyWorker.get_worker_by_id_with_position(current_user.get_id())

        return render_template('head/head_page.html', that_user=that_user)
    else:
        return render_template('head/head_page.html')


# Редактирование профиля работника: фото, номер телефона, ФИО
@head.route('/new-adders-for-profile', methods=['GET', 'POST'])
@login_required
def update_profile_page():
    # Форма для обновления сотрудника
    worker_update_form = UpdateWorker()

    # Получение текущей информации о сотруднике - возможность обновлять данные частично
    that_user = CompanyWorker.get_worker_by_id_with_position(current_user.get_id())

    # Обновление информации о работнике
    if worker_update_form.submit_update.data:
        # Проверка введённого ФИО
        if worker_update_form.fio.data:
            fio_update = worker_update_form.fio.data
        else:
            fio_update = that_user.CompanyWorker.fio

        # Проверка введённого телефона
        if worker_update_form.phone_number.data:
            phone_number_update = worker_update_form.phone_number.data
        else:
            phone_number_update = that_user.CompanyWorker.phone_number

        # Проверка введённой ссылки на фото
        if worker_update_form.user_photo.data:
            photo_update = worker_update_form.user_photo.data
        else:
            photo_update = that_user.CompanyWorker.photo

        # Вызов метода обновления сотрудника в базе
        CompanyWorker.update_company_worker(current_user.get_id(), fio_update, phone_number_update, photo_update)

        return redirect(url_for('head.set_profile_page'))

    return render_template('head/profile_update_page.html', that_user=that_user, worker_update_form=worker_update_form)
