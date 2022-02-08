from flask import render_template, Blueprint, redirect, url_for, session, flash
from software_app.models import Project, Task
from flask_login import login_required, current_user
from software_app.forms import IdProjectByPress


project = Blueprint('project', __name__, template_folder="templates")


@project.route('/all_projects', methods=['GET', 'POST'])
@login_required
def project_view():
    all_projects = Project.get_all_projects()
    press_form = IdProjectByPress()

    if press_form.submit.data:
        return redirect(url_for('project.project_info', id_project=press_form.id_project_for_info.data))

    return render_template('project/all_projects.html', all_projects=all_projects, press_form=press_form)


@project.route('/project-info/<int:id_project>', methods=['GET', 'POST'])
@login_required
def project_info(id_project):
    project_for_view = Project.get_project_by_id(id_project)
    all_tasks_project = Task.get_all_tasks_by_project_id(id_project)
    return render_template('project/all_tasks_project.html', project_for_view=project_for_view,
                           all_tasks_project=all_tasks_project)


@project.route('/my_projects', methods=['GET', 'POST'])
@login_required
def supervisor_view():
    if session['post'] == 5:
        all_projects = Project.get_all_projects_by_id_supervisor(current_user.get_id())

        return render_template('project/supervisor_projects.html', all_projects=all_projects)
    else:
        flash('У вас недостаточно прав для доступа к этой странице', category='danger')
        return redirect(url_for('head.set_profile_page'))
