from flask_login import UserMixin
from software_app import db
from software_app import login_manager
from software_app import bcrypt
from flask import flash


# Подключение загрузки пользователя: ID пользователя в логин-менеджере
@login_manager.user_loader
def load_user(user_id):
    return CompanyWorker.query.get(int(user_id))


# Класс с информацией о рабочем
class CompanyWorker(db.Model, UserMixin):
    __tablename__ = 'company_worker'
    __table_args__ = {'extend_existing': True}

    id_company_worker = db.Column(db.Integer(), primary_key=True)
    password = db.Column(db.String(length=150), nullable=False)

    # Метод получения ID пользователя из таблицы
    def get_id(self):
        return self.id_company_worker

    # Метод возвращения пароля
    @property
    def unencrypted_password(self):
        return self.unencrypted_password

    # Метод шифрования пароля для БД
    @unencrypted_password.setter
    def unencrypted_password(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    # Метод проверки пароля
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)

    # Метод получения работника по ID с позицией
    @staticmethod
    def get_worker_by_id_with_position(id_company_worker):
        query = db.session.query(CompanyWorker, WorkerPost)
        query = query.join(WorkerPost, CompanyWorker.id_worker_post == WorkerPost.id_worker_post)
        query = query.filter(CompanyWorker.id_company_worker == id_company_worker).first()
        return query

    # Метод получения работника по ID
    @staticmethod
    def get_worker_by_id(id_company_worker):
        return CompanyWorker.query.filter_by(id_company_worker=id_company_worker).first()

    # Метод получения работника по логину
    @staticmethod
    def get_worker_by_login(login):
        return CompanyWorker.query.filter_by(login=login).first()

    # Метод получения работника по ФИО
    @staticmethod
    def get_worker_by_fio(fio):
        return CompanyWorker.query.filter_by(fio=fio).first()

    # Метод добавления работника
    @staticmethod
    def add_company_worker(fio, type_work, phone_number, login, password, id_worker_post, photo=None):
        new_company_worker = CompanyWorker(fio=fio, phone_number=phone_number, login=login, type_work=type_work,
                                           unencrypted_password=password, id_worker_post=id_worker_post, photo=photo)

        try:
            db.session.add(new_company_worker)
            db.session.commit()
            flash("Сотрудник был успешно добавлен.", category='success')
        except:
            db.session.rollback()
            flash("Произошла ошибка при добавлении сотрудника. Повторите попытку.", category='danger')

    # Метод обновления информации о работнике
    @staticmethod
    def update_company_worker(id_company_worker, fio, phone_number, photo):
        try:
            worker_for_update = CompanyWorker.get_worker_by_id(id_company_worker)
            worker_for_update.fio = fio
            worker_for_update.phone_number = phone_number
            worker_for_update.photo = photo
            db.session.commit()
            flash("Сотрудник был успешно изменён.", category='success')
        except:
            db.session.rollback()
            flash("Произошла ошибка при измении данных сотрудника. Повторите попытку.", category='danger')


# Класс с информацией о выполнении заданий
class WorkerExecution(db.Model):
    __tablename__ = 'worker_execution'
    __table_args__ = {'extend_existing': True}

    # Метод добавления исполнения в задании
    @staticmethod
    def add_execution(id_project, id_task, id_executor, iteration_number, start_date, finish_date, id_status):
        new_execution = WorkerExecution(id_project=id_project, id_task=id_task, id_executor=id_executor,
                                        iteration_number=iteration_number, start_date=start_date,
                                        finish_date=finish_date, id_status=id_status)
        try:
            db.session.add(new_execution)
            db.session.commit()
            flash("Задача была взята в обработку.", category='success')
        except:
            db.session.rollback()
            flash("Произошла ошибка при обработке задачи. Повторите попытку.", category='danger')

    # Метод получения всех задач на исполнении
    @staticmethod
    def get_all_task_by_id_executor(id_executor):
        query = db.session.query(WorkerExecution, Project, CompanyWorker, Status, Task)
        query = query.join(Project, WorkerExecution.id_project == Project.id_project)
        query = query.join(CompanyWorker, Project.id_supervisor == CompanyWorker.id_company_worker)
        query = query.join(Status, Status.id_status == WorkerExecution.id_status)
        query = query.join(Task, Task.id_task == WorkerExecution.id_task)
        query = query.filter(WorkerExecution.id_executor == id_executor)
        return query.all()

    # Метод обновления задачи на исполнении
    @staticmethod
    def update_task_execution_by_id(id_task, id_status, iteration_number):
        try:
            execute_task_for_update = WorkerExecution.query.filter_by(id_task=id_task).first()
            execute_task_for_update.id_status = id_status
            execute_task_for_update.iteration_number = iteration_number
            db.session.commit()
            flash("Статус и итерация задачи были успешно изменены", category='success')
        except:
            db.session.rollback()
            flash("Изменения не были внесены", category='danger')

    # Метод удаления задачи на исполнении
    @staticmethod
    def delete_task_execution_by_id(id_task):
        try:
            WorkerExecution.query.filter_by(id_task=id_task).delete()
            db.session.commit()
            flash("Отказ от задания был успешно выполнен", category='success')
        except:
            db.session.rollback()
            flash("Удаление прошло неудачно", category='danger')


# Класс с информацией о всех проектах
class Project(db.Model):
    __tablename__ = 'project'
    __table_args__ = {'extend_existing': True}

    # Метод получения всех проектов
    @staticmethod
    def get_all_projects():
        query = db.session.query(Project, State, CompanyWorker)
        query = query.join(State, Project.id_project_state == State.id_state)
        query = query.join(CompanyWorker, Project.id_supervisor == CompanyWorker.id_company_worker).all()
        return query

    # Метод получения проекта по ID
    @staticmethod
    def get_project_by_id(id_project):
        return Project.query.filter_by(id_project=id_project).first()

    # Метод получения проектов по ID руководителя
    @staticmethod
    def get_all_projects_by_id_supervisor(id_supervisor):
        query = db.session.query(Project, State, CompanyWorker)
        query = query.join(State, Project.id_project_state == State.id_state)
        query = query.join(CompanyWorker, Project.id_supervisor == CompanyWorker.id_company_worker)
        query = query.filter(Project.id_supervisor == id_supervisor).all()
        return query

    # Метод добавления нового проекта
    @staticmethod
    def add_project(name_project, type_project, completion_date, project_laboriousness, id_supervisor,
                    id_project_state):
        new_project = Project(name_project=name_project, type_project=type_project, completion_date=completion_date,
                              project_laboriousness=project_laboriousness, id_supervisor=id_supervisor,
                              id_project_state=id_project_state)

        try:
            db.session.add(new_project)
            db.session.commit()
            flash("Новый проект был успешно добавлен", category='success')
        except:
            db.session.rollback()
            flash("Возникли проблемы с добавление нового проекта", category='danger')

    # Метод обновления проекта
    @staticmethod
    def update_project_by_id(id_project, id_state):
        try:
            project_for_update = Project.query.filter_by(id_project=id_project).first()
            project_for_update.id_project_state = id_state
            db.session.commit()
            flash("Состояние проекта было успешно изменено", category='success')
        except:
            db.session.rollback()
            flash("Изменения не были внесены", category='danger')

    # Метод удаления (закрытия) проекта
    @staticmethod
    def delete_project_by_id(id_project):
        try:
            Project.query.filter_by(id_project=id_project).delete()
            db.session.commit()
            flash("Проект был успешно закрыт", category='success')
        except:
            db.session.rollback()
            flash("Произошла ошибка при закрытии проекта", category='danger')


# Таблица с состояними для проекта
class State(db.Model):
    __tablename__ = 'state'
    __table_args__ = {'extend_existing': True}

    # Метод получения всех проектов
    @staticmethod
    def get_all_state():
        return State.query.all()

    # Метод получения состояния по его названию
    @staticmethod
    def get_state_by_name(name_state):
        return State.query.filter_by(name_state=name_state).first()


# Таблица со статусами для заданий
class Status(db.Model):
    __tablename__ = 'status'
    __table_args__ = {'extend_existing': True}

    # Методу получения всех статусов
    @staticmethod
    def get_all_status():
        return Status.query.all()

    # Метод получения статуса по его названию
    @staticmethod
    def get_status_by_name(name_status):
        return Status.query.filter_by(name_status=name_status).first()


# Таблица с заданиями
class Task(db.Model):
    __tablename__ = 'task'
    __table_args__ = {'extend_existing': True}

    # Метод получения свободных задач
    @staticmethod
    def get_all_free_tasks_by_project_id(id_project):
        query = db.session.query(Task, WorkerExecution)
        query = query.outerjoin(WorkerExecution)
        query = query.filter(None == WorkerExecution.id_task)
        query = query.filter(Task.id_project == id_project)
        return query.all()

    # Метод получения всех задач в исполнении
    @staticmethod
    def get_all_not_free_tasks_by_project_id(id_project):
        query = db.session.query(Task, WorkerExecution, CompanyWorker, Status)
        query = query.join(WorkerExecution, Task.id_task == WorkerExecution.id_task)
        query = query.join(CompanyWorker, WorkerExecution.id_executor == CompanyWorker.id_company_worker)
        query = query.join(Status, WorkerExecution.id_status == Status.id_status)
        query = query.filter(Task.id_project == id_project)
        return query.all()

    # Метод добавления новой задачи
    @staticmethod
    def add_task(dateadd, task_laboriousness, id_project, description, duration):
        new_task = Task(dateadd=dateadd, task_laboriousness=task_laboriousness, id_project=id_project,
                        description=description, duration=duration)

        try:
            db.session.add(new_task)
            db.session.commit()
            flash("Новое задание было успешно добавлено в проект", category='success')
        except:
            db.session.rollback()
            flash("Возникли проблемы с добавление нового задания в проект", category='danger')

    # Метод удаления задачи по ID
    @staticmethod
    def delete_task_by_id(id_task):
        try:
            Task.query.filter_by(id_task=id_task).delete()
            db.session.commit()
            flash("Задача была успешно удалена", category='success')
        except:
            db.session.rollback()
            flash("Произошла ошибка при удалении задачи", category='danger')


# Таблица с должностями работников
class WorkerPost(db.Model):
    __tablename__ = 'worker_post'
    __table_args__ = {'extend_existing': True}

    # Метод получения всех должностей
    @staticmethod
    def get_all_worker_posts():
        return WorkerPost.query.all()

    # Метод получения информации должности об имени
    @staticmethod
    def get_worker_post_by_name(name_worker_post):
        return WorkerPost.query.filter_by(name_worker_post=name_worker_post).first()
