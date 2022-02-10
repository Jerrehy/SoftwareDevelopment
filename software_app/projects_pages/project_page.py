from flask import render_template, Blueprint, redirect, url_for, session, flash
from software_app.models import Project, Task, State, WorkerExecution
from flask_login import login_required, current_user
from software_app.forms import IdProjectByPress, AddProject, IdProjectAndTaskByPress, UpdateProject, CloseProject
from datetime import timedelta


# Создание узла связанного с проектами
project = Blueprint('project', __name__, template_folder="templates")


# Просмотр всех проектов команды для работников (для руководителя отдельно)
@project.route('/all_projects', methods=['GET', 'POST'])
@login_required
def project_view():
    if session['post'] != 5:
        # Вывод всех проектов
        all_projects = Project.get_all_projects()

        # Подключение формы для проектов
        press_form = IdProjectByPress()

        # Переключение на узел со списком заданий по ID проекта
        if press_form.submit.data:
            return redirect(url_for('project.project_info', id_project=press_form.id_project_for_info.data))

        return render_template('project/all_projects.html', all_projects=all_projects, press_form=press_form)
    else:
        flash('У вас недостаточно прав для доступа к этой странице', category='danger')
        return redirect(url_for('head.set_profile_page'))


# Просмотр заданий проекта по ID и выбор свободных заданий работником
@project.route('/project-info/<int:id_project>', methods=['GET', 'POST'])
@login_required
def project_info(id_project):
    if session['post'] != 5:
        # Активация нового задания
        activation_form = IdProjectAndTaskByPress()

        # Информация о проекте по ID
        project_for_view = Project.get_project_by_id(id_project)
        # Все свободные задачи по проекту
        all_free_tasks_project = Task.get_all_free_tasks_by_project_id(id_project)
        # Все занятые задачи по проекты
        all_not_free_tasks_project = Task.get_all_not_free_tasks_by_project_id(id_project)

        if activation_form.submit_add.data:
            # Получение даты окончания задачи по длительности выполнения задачи
            date_summary = activation_form.start_date.data
            result = date_summary + timedelta(days=int(activation_form.duration_for_info.data))
            result = result.strftime('%Y-%m-%d')

            # Добавление информации о выполнении задачи работником
            WorkerExecution.add_execution(id_project, activation_form.id_task_for_info.data,
                                          current_user.get_id(), activation_form.iteration.data,
                                          activation_form.start_date.data, result, 2)

            return redirect(url_for('project.project_info', id_project=id_project))

        return render_template('project/all_tasks_project.html', project_for_view=project_for_view,
                               all_free_tasks_project=all_free_tasks_project, activation_form=activation_form,
                               all_not_free_tasks_project=all_not_free_tasks_project)
    else:
        flash('У вас недостаточно прав для доступа к этой странице', category='danger')
        return redirect(url_for('head.set_profile_page'))


# Просмотр руководителем его проектов
@project.route('/my_projects', methods=['GET', 'POST'])
@login_required
def supervisor_view():
    if session['post'] == 5:
        # Форма для добавления проекта
        form_add_project = AddProject()
        # Форма для обновления проекта
        form_update_project = UpdateProject()
        # Форма для удаления проекта
        form_close_project = CloseProject()
        # Форма перехода к узлу со списком заданий к проекту - специально для руководителя
        press_form = IdProjectByPress()

        # Получение списка состояний проекта из БД
        projects_states = State.get_all_state()
        # Ввод списка состояний в форму добавления проекта
        form_add_project.project_state.choices = [i.name_state for i in projects_states]
        # Ввод списка состояний в форму обновления списка
        form_update_project.new_state_project.choices = [i.name_state for i in projects_states]

        # Получение списка всех проектов по ID руководителя
        all_projects = Project.get_all_projects_by_id_supervisor(current_user.get_id())

        # Активация метода добавления проекта
        if form_add_project.validate_on_submit():
            project_state = State.get_state_by_name(form_add_project.project_state.data)
            Project.add_project(form_add_project.project_name.data, form_add_project.project_type.data,
                                form_add_project.deadline.data, form_add_project.laboriousness.data, current_user.get_id(),
                                project_state.id_state)
            return redirect(url_for('project.supervisor_view'))

        # Активация метода обновления проекта
        elif form_update_project.submit_update.data:
            new_state_for_project = State.get_state_by_name(form_update_project.new_state_project.data)
            Project.update_project_by_id(form_update_project.id_project_for_update.data, new_state_for_project.id_state)
            return redirect(url_for('project.supervisor_view'))

        # Активация метода удаления проекта
        elif form_close_project.submit_close.data:
            Project.delete_project_by_id(form_close_project.id_project_for_close.data)
            return redirect(url_for('project.supervisor_view'))

        # Активация метода перехода на страницу с заданиями проектами
        elif press_form.submit.data:
            return redirect(url_for('task.task_view_for_supervisor', id_project=press_form.id_project_for_info.data))

        return render_template('project/supervisor_projects.html', all_projects=all_projects,
                               form_add_project=form_add_project, form_update_project=form_update_project,
                               form_close_project=form_close_project, press_form=press_form)
    else:
        flash('У вас недостаточно прав для доступа к этой странице', category='danger')
        return redirect(url_for('head.set_profile_page'))

