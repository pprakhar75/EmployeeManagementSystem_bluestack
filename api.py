from os import urandom
from functools import wraps
from constants import errors, ROLE
from flask import Flask, request, render_template, redirect, url_for, session
from controller import show_employee_details, mark_employee_deleted, edit_employee, \
    add_employee_to_db, search_employee_details, get_emp_role, login_user, logout_user, is_logged_in

app = Flask(__name__)

app.secret_key = urandom(24)


def roles_required(*required_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get('emp_id'):
                emp_role = get_emp_role(session['emp_id'])
                if emp_role not in required_roles:
                    return render_template('PermissionDenied.html')
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def login_required():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('emp_id') or not is_logged_in(session.get('emp_id')):
                return render_template('login.html', errors=errors['re_login'])
            return f(*args, **kwargs)

        return decorated_function

    return decorator


@app.route('/home')
@roles_required(ROLE['admin'], ROLE['eng_manager'], ROLE['default'])
def index(emp_id=None, login_status=None):
    if request.args:
        for i in request.args.items():
            emp_id = i[1]
    return render_template('index_2.html', employee_data=show_employee_details(),
                           search_employee_data=search_employee_details(emp_id=emp_id))


@app.route('/add', methods=['POST'])
@roles_required(ROLE['admin'], ROLE['eng_manager'])
@login_required()
def add():
    """
    this function takes the post request for addition of the empoloyee in database
    :return: redirect to the index
    """
    if not session['emp_id']:
        return render_template('login.html', error=errors['re_login'])
    add_employee_to_db(request.form)
    return redirect(url_for('index'))


@app.route('/delete/<int:emp_id>', methods=['POST'])
@roles_required(ROLE['admin'])
def delete(emp_id):
    """
    This function takes the empid as the request parameter and delete the  employee from the database
    :param emp_id:
    :return: redirect to index
    """
    if emp_id:
        mark_employee_deleted(emp_id=emp_id)
        return redirect(url_for('index'))


@app.route('/edit', methods=['POST'])
@roles_required(ROLE['admin'], ROLE['eng_manager'])
def edit():
    """
    this function takes the post request and edit the employee
    :return: redirect to url
    """
    edit_employee(request.form)
    return redirect(url_for('index'))


# Route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        login_status = login_user(employee_details=request.form)
        if not login_status:
            error = errors['invalid_credentials']
        else:
            session['emp_id'] = request.form['emp_id']
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout', methods=['GET'])
def logout():
    logout_user(session['emp_id'])
    session.pop('emp_id')
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
# check for the login status
# e to e testing
# postman testing
