from flask import render_template, Blueprint
from software_app.models import Project
from flask_login import login_required


project = Blueprint('project', __name__, template_folder="templates")


@project.route('/all_projects', methods=['GET', 'POST'])
@login_required
def project_view():
    all_projects = Project.get_all_projects()
    return render_template('project/all_projects.html', all_projects=all_projects)
