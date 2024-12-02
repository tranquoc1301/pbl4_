from flask import request, flash
from website import db
from website.models.department_salary import DepartmentSalary


def get_all_department_salary():
    return DepartmentSalary.query.all()


def get_department_salary_by_id(department_id):
    return DepartmentSalary.query.filter_by(department_id=department_id).first()


def update_department_salary(department_id, hourly_salary):
    department_salary = get_department_salary_by_id(department_id).first()
    department_salary.hourly_salary = hourly_salary
    try:
        db.session.commit()
        return "", 200
    except Exception as e:
        db.session.rollback()
        flash('Lỗi: ' + str(e), 'danger')
        return "", 400
