from flask import Blueprint, render_template

head = Blueprint('head', __name__, template_folder="templates")


# Начальная страница сайта
@head.route('/')
@head.route('/head', methods=['GET'])
def set_profile_page():
    return render_template('head/head_page.html')
