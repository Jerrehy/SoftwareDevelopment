from flask import render_template, Blueprint, redirect, url_for, session, flash
from software_app.models import WorkerExecution, Status
from software_app.forms import UpdateTaskExecution, RejectTaskExecution
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
