from flask import Blueprint, render_template, flash, redirect, url_for
from ..auth import login_required
from ..controllers.users_controller import (
    get_all_users,
    get_user_by_id,
    create_user as create_user_service,
    update_user as update_user_service,
    delete_user as delete_user_service
)
from ..authorize import role_required
user_bp = Blueprint('user', __name__)


@user_bp.route('/')
@login_required
@role_required([1])
def index():
    users = get_all_users()
    return render_template('admin/user/index.html', users=users)


@user_bp.route('/create', methods=['POST'])
@login_required
@role_required([1])
def create():
    message, status = create_user_service()
    flash(message, category='success' if status == 201 else 'danger')
    return redirect(url_for('user.index'))


@user_bp.route('/update/<int:user_id>', methods=['POST'])
@login_required
@role_required([1])
def update(user_id):
    message, status = update_user_service(user_id)
    flash(message, category='success' if status == 200 else 'danger')
    return redirect(url_for('user.index'))


@user_bp.route('/delete/<int:user_id>', methods=['POST'])
@login_required
@role_required([1])
def delete(user_id):
    message, status = delete_user_service(user_id)
    flash(message, category='success' if status == 200 else 'danger')
    return redirect(url_for('user.index'))
