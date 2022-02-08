from flask import render_template, Blueprint, redirect, url_for, session, flash
from software_app.models import WorkerExecution
from flask_login import login_required, current_user

task = Blueprint('task', __name__, template_folder="templates")


@task.route('/all_worker_tasks', methods=['GET', 'POST'])
@login_required
def task_view():
    if session['post'] != 5:
        all_worker_tasks = WorkerExecution.get_all_task_by_id_executor(current_user.get_id())
        return render_template('task/worker_tasks.html', all_worker_tasks=all_worker_tasks)
    else:
        flash('У вас недостаточно прав для доступа к этой странице', category='danger')
        return redirect(url_for('head.set_profile_page'))
