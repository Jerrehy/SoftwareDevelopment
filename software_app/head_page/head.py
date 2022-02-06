from flask import Blueprint, render_template, session
from flask_login import current_user
from software_app.models import CompanyWorker

head = Blueprint('head', __name__, template_folder="templates")


# Начальная страница сайта
@head.route('/')
@head.route('/head', methods=['GET'])
def set_profile_page():
    if current_user.is_authenticated:
        that_user = CompanyWorker.get_worker_by_id_with_position(current_user.get_id())
        return render_template('head/head_page.html', that_user=that_user)
    else:
        return render_template('head/head_page.html')
