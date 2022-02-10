from flask import render_template, Blueprint, redirect, url_for, session, flash
from software_app.models import WorkerExecution, Status, Project, Task
from software_app.forms import UpdateTaskExecution, RejectTaskExecution, AddTask, DeleteTask
from flask_login import login_required, current_user

# Создание узла связанного с задачи
task = Blueprint('task', __name__, template_folder="templates")


# Узёл с заданиями всех пользователей
@task.route('/all_worker_tasks', methods=['GET', 'POST'])
@login_required
def task_view():
    if session['post'] != 5:
        # Форма обновления задания исполнителя для рабочего
        update_form = UpdateTaskExecution()
        # Форма удаления задания исполнителя (отказ) для рабочего
        reject_form = RejectTaskExecution()

        # Получение списка всех доступных статусов проекта
        status_for_from = Status.get_all_status()
        # Заполнение формы обновления задания исполнителя
        update_form.new_status_task.choices = [i.name_status for i in status_for_from]
        # Список всех заданий пользователя
        all_worker_tasks = WorkerExecution.get_all_task_by_id_executor(current_user.get_id())

        # Метод изменения статуса задания на исполнении у рабочего
        if update_form.submit_update.data:
            status_for_update = Status.get_status_by_name(update_form.new_status_task.data)
            WorkerExecution.update_task_execution_by_id(update_form.id_task_for_update.data,
                                                        status_for_update.id_status, update_form.new_iteration.data)
            return redirect(url_for('task.task_view'))

        # Метод отказа от исполнения задания на исполнении у рабочего
        elif reject_form.submit_reject.data:
            WorkerExecution.delete_task_execution_by_id(reject_form.id_task_for_reject.data)
            return redirect(url_for('task.task_view'))

        return render_template('task/worker_tasks.html', all_worker_tasks=all_worker_tasks, update_form=update_form,
                               reject_form=reject_form)

    else:
        flash('У вас недостаточно прав для доступа к этой странице', category='danger')
        return redirect(url_for('head.set_profile_page'))


# Узел со всеми заданиями для просмотра руководителем проекта
@task.route('/all_worker_tasks_for_supervisor/<int:id_project>', methods=['GET', 'POST'])
@login_required
def task_view_for_supervisor(id_project):
    if session['post'] == 5:

        task_adder = AddTask()
        update_form = UpdateTaskExecution()
        delete_form = DeleteTask()

        status_for_from = Status.get_all_status()
        update_form.new_status_task.choices = [i.name_status for i in status_for_from]

        project_for_view = Project.get_project_by_id(id_project)
        all_free_tasks_project = Task.get_all_free_tasks_by_project_id(id_project)
        all_not_free_tasks_project = Task.get_all_not_free_tasks_by_project_id(id_project)

        if task_adder.submit_add.data:
            Task.add_task(task_adder.date_now.data, task_adder.laboriousness.data, id_project,
                          task_adder.description.data, task_adder.duration.data)
            return redirect(url_for('task.task_view_for_supervisor', id_project=id_project))

        elif update_form.submit_update.data:
            status_for_update = Status.get_status_by_name(update_form.new_status_task.data)
            WorkerExecution.update_task_execution_by_id(update_form.id_task_for_update, status_for_update.id_status,
                                                        update_form.new_iteration.data)
            return redirect(url_for('task.task_view_for_supervisor', id_project=id_project))

        elif delete_form.submit_delete.data:
            Task.delete_task_by_id(delete_form.id_task_for_delete.data)
            return redirect(url_for('task.task_view_for_supervisor', id_project=id_project))

        return render_template('task/worker_tasks_for_supervisor.html', project_for_view=project_for_view,
                               all_free_tasks_project=all_free_tasks_project, task_adder=task_adder,
                               update_form=update_form, all_not_free_tasks_project=all_not_free_tasks_project,
                               delete_form=delete_form)

    else:
        flash('У вас недостаточно прав для доступа к этой странице', category='danger')
        return redirect(url_for('head.set_profile_page'))
