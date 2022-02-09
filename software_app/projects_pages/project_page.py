from flask import render_template, Blueprint, redirect, url_for, session, flash
from software_app.models import Project, Task, State, WorkerExecution
from flask_login import login_required, current_user
from software_app.forms import IdProjectByPress, AddProject, IdProjectAndTaskByPress, UpdateProject, CloseProject
from datetime import timedelta


project = Blueprint('project', __name__, template_folder="templates")


@project.route('/all_projects', methods=['GET', 'POST'])
@login_required
def project_view():
    if session['post'] != 5:
        all_projects = Project.get_all_projects()
        press_form = IdProjectByPress()

        if press_form.submit.data:
            return redirect(url_for('project.project_info', id_project=press_form.id_project_for_info.data))

        return render_template('project/all_projects.html', all_projects=all_projects, press_form=press_form)
    else:
        flash('У вас недостаточно прав для доступа к этой странице', category='danger')
        return redirect(url_for('head.set_profile_page'))


@project.route('/project-info/<int:id_project>', methods=['GET', 'POST'])
@login_required
def project_info(id_project):
    if session['post'] != 5:
        activation_form = IdProjectAndTaskByPress()

        project_for_view = Project.get_project_by_id(id_project)
        all_free_tasks_project = Task.get_all_free_tasks_by_project_id(id_project)
        all_not_free_tasks_project = Task.get_all_not_free_tasks_by_project_id(id_project)

        if activation_form.submit_add.data:

            date_summary = activation_form.start_date.data
            result = date_summary + timedelta(days=int(activation_form.duration_for_info.data))
            result = result.strftime('%Y-%m-%d')

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


@project.route('/my_projects', methods=['GET', 'POST'])
@login_required
def supervisor_view():
    if session['post'] == 5:
        form_add_project = AddProject()
        form_update_project = UpdateProject()
        form_close_project = CloseProject()
        press_form = IdProjectByPress()

        projects_states = State.get_all_state()
        form_add_project.project_state.choices = [i.name_state for i in projects_states]
        form_update_project.new_state_project.choices = [i.name_state for i in projects_states]

        all_projects = Project.get_all_projects_by_id_supervisor(current_user.get_id())

        if form_add_project.validate_on_submit():
            project_state = State.get_state_by_name(form_add_project.project_state.data)
            Project.add_project(form_add_project.project_name.data, form_add_project.project_type.data,
                                form_add_project.deadline.data, form_add_project.laboriousness.data, current_user.get_id(),
                                project_state.id_state)
            return redirect(url_for('project.supervisor_view'))

        elif form_update_project.submit_update.data:
            new_state_for_project = State.get_state_by_name(form_update_project.new_state_project.data)
            Project.update_project_by_id(form_update_project.id_project_for_update.data, new_state_for_project.id_state)
            return redirect(url_for('project.supervisor_view'))

        elif form_close_project.submit_close.data:
            Project.delete_project_by_id(form_close_project.id_project_for_close.data)
            return redirect(url_for('project.supervisor_view'))

        elif press_form.submit.data:
            return redirect(url_for('task.task_view_for_supervisor', id_project=press_form.id_project_for_info.data))

        return render_template('project/supervisor_projects.html', all_projects=all_projects,
                               form_add_project=form_add_project, form_update_project=form_update_project,
                               form_close_project=form_close_project, press_form=press_form)
    else:
        flash('У вас недостаточно прав для доступа к этой странице', category='danger')
        return redirect(url_for('head.set_profile_page'))

