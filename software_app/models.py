from flask_login import UserMixin
from software_app import db
from software_app import login_manager
from software_app import bcrypt
from flask import flash


@login_manager.user_loader
def load_user(user_id):
    return CompanyWorker.query.get(int(user_id))


class CompanyWorker(db.Model, UserMixin):
    __tablename__ = 'company_worker'
    __table_args__ = {'extend_existing': True}

    id_company_worker = db.Column(db.Integer(), primary_key=True)
    password = db.Column(db.String(length=150), nullable=False)

    # Метод получения ID пользователя из таблицы
    def get_id(self):
        return self.id_company_worker

    @property
    def unencrypted_password(self):
        return self.unencrypted_password

    @unencrypted_password.setter
    def unencrypted_password(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)

    @staticmethod
    def get_worker_by_id_with_position(id_company_worker):
        query = db.session.query(CompanyWorker, WorkerPost)
        query = query.join(WorkerPost, CompanyWorker.id_worker_post == WorkerPost.id_worker_post)
        query = query.filter(CompanyWorker.id_company_worker == id_company_worker).first()
        return query

    @staticmethod
    def get_worker_by_login(login):
        return CompanyWorker.query.filter_by(login=login).first()

    @staticmethod
    def get_worker_by_fio(fio):
        return CompanyWorker.query.filter_by(fio=fio).first()

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


class WorkerExecution(db.Model):
    __tablename__ = 'worker_execution'
    __table_args__ = {'extend_existing': True}


class Project(db.Model):
    __tablename__ = 'project'
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def get_all_projects():
        query = db.session.query(Project, State, CompanyWorker)
        query = query.join(State, Project.id_project_state == State.id_state)
        query = query.join(CompanyWorker, Project.id_supervisor == CompanyWorker.id_company_worker)
        return query.all()


class State(db.Model):
    __tablename__ = 'state'
    __table_args__ = {'extend_existing': True}


class Status(db.Model):
    __tablename__ = 'status'
    __table_args__ = {'extend_existing': True}


class Task(db.Model):
    __tablename__ = 'task'
    __table_args__ = {'extend_existing': True}


class WorkerPost(db.Model):
    __tablename__ = 'worker_post'
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def get_all_worker_posts():
        return WorkerPost.query.all()

    @staticmethod
    def get_worker_post_by_name(name_worker_post):
        return WorkerPost.query.filter_by(name_worker_post=name_worker_post).first()
