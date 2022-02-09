from flask import render_template, Blueprint, redirect, url_for, session, flash
from software_app.models import WorkerExecution, Status, Project, Task
from software_app.forms import UpdateTaskExecution, RejectTaskExecution, AddTask, DeleteTask
from flask_login import login_required, current_user

task = Blueprint('task', __name__, template_folder="templates")


@task.route('/all_worker_tasks', methods=['GET', 'POST'])
@login_required
def task_view():
    if session['post'] != 5:
        update_form = UpdateTaskExecution()
        reject_form = RejectTaskExecution()

        status_for_from = Status.get_all_status()
        update_form.new_status_task.choices = [i.name_status for i in status_for_from]

        all_worker_tasks = WorkerExecution.get_all_task_by_id_executor(current_user.get_id())

        if update_form.submit_update.data:
            status_for_update = Status.get_status_by_name(update_form.new_status_task.data)
            WorkerExecution.update_task_execution_by_id(update_form.id_task_for_update.data,
                                                        status_for_update.id_status, update_form.new_iteration.data)
            return redirect(url_for('task.task_view'))

        elif reject_form.submit_reject.data:
            WorkerExecution.delete_task_execution_by_id(reject_form.id_task_for_reject.data)
            return redirect(url_for('task.task_view'))

        return render_template('task/worker_tasks.html', all_worker_tasks=all_worker_tasks, update_form=update_form,
                               reject_form=reject_form)

    else:
        flash('У вас недостаточно прав для доступа к этой странице', category='danger')
        return redirect(url_for('head.set_profile_page'))


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

        return render_template('task/worker_tasks_for_supervisor.html', project_for_view=project_for_view,
                               all_free_tasks_project=all_free_tasks_project, task_adder=task_adder,
                               update_form=update_form, all_not_free_tasks_project=all_not_free_tasks_project,
                               delete_form=delete_form)

    else:
        flash('У вас недостаточно прав для доступа к этой странице', category='danger')
        return redirect(url_for('head.set_profile_page'))
