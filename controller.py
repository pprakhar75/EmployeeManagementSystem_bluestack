from model import Session, Employee
from sqlalchemy import and_
from functools import wraps
from flask import render_template

session = Session()


def add_employee_to_db(employee_details):
    if employee_details:
        print(employee_details)
        row = Employee(employee_name=employee_details['employee_name'],
                       employee_gender=employee_details['employee_gender'],
                       password=employee_details['password'],
                       employee_role=employee_details['employee_role'],
                       login_status='p')
        session.add(row)
        session.commit()
        return 'Employee added successfully'


def search_employee_details(emp_id=None):
    if emp_id:
        all_employee = session.query(Employee).filter_by(emp_id=emp_id).all()
        data = {}
        for i in all_employee:
            employee_data = {}
            employee_data['emp_id'] = i.emp_id
            employee_data['employee_name'] = i.employee_name
            employee_data['employee_gender'] = i.employee_gender
            employee_data['employee_role'] = i.employee_role
            data[i.emp_id] = employee_data  # todo to understand
        return data
    else:
        return {}


def show_employee_details(emp_id=None, login_status=None):
    data = {}
    if emp_id:
        all_employee = session.query(Employee).filter(and_(Employee.login_status != 'd', Employee.emp_id == emp_id))
        print('in show emplpyee details', all_employee)
    else:
        all_employee = session.query(Employee).filter(Employee.login_status != 'd')
        print('in show emplpyee details', all_employee)
        if not all_employee:
            data = None

    for i in all_employee:
        employee_data = {}
        employee_data['emp_id'] = i.emp_id
        employee_data['employee_name'] = i.employee_name
        employee_data['employee_gender'] = i.employee_gender
        employee_data['employee_role'] = i.employee_role
        data[i.emp_id] = employee_data  # todo to understand

    return data


def mark_employee_deleted(emp_id):
    employee_detail = session.query(Employee).filter_by(emp_id=emp_id).first()
    employee_detail.login_status = 'd'
    session.commit()


def edit_employee(employee_edit_details=None):
    print('inside edit employee details', employee_edit_details)
    employee_detail = session.query(Employee).filter_by(emp_id=employee_edit_details['employee_id']).first()
    if employee_detail:
        if employee_edit_details.get('employee_name'):
            employee_detail.employee_name = employee_edit_details['employee_name']
        if employee_edit_details.get('employee_gender'):
            employee_detail.employee_gender = employee_edit_details['employee_gender']
        if employee_edit_details.get('employee_role'):
            employee_detail.employee_role = employee_edit_details['employee_role']
        session.commit()
        return True
    else:
        return False


def is_logged_in(emp_id):
    employee_details = session.query(Employee).filter_by(emp_id=emp_id).first()
    if employee_details:
        login_status = employee_details.login_status
        if login_status == 'a':
            return True
        else:
            return False  # todo return meaningful return message may be authentication error
    else:
        return False  # todo return employee not found


def get_emp_role(emp_id):
    employee_details = session.query(Employee).filter_by(emp_id=emp_id).first()
    if employee_details:
        emp_role = employee_details.employee_role
        return emp_role
    else:
        return False  # todo return employee not found


def login_user(employee_details):
    employee_data = session.query(Employee).filter_by(emp_id=employee_details['emp_id']).first()
    if employee_data and employee_data.login_status != 'd' and employee_data.password == employee_details['password']:
        employee_data.login_status = 'a'  # if user exist mark user logged in.
        session.commit()
        return True
    else:
        return False


def logout_user(emp_id):
    employee_data = session.query(Employee).filter_by(emp_id=emp_id).first()
    if employee_data:
        employee_data.login_status = 'p'
        session.commit()
        return True
    else:
        return False


def roles_required(*required_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            emp_role = get_emp_role(session.get('emp_id'))
            if emp_role not in required_roles:
                return render_template('PermissionDenied.html')
            return f(*args, **kwargs)

        return decorated_function

    return decorator
