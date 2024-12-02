from functools import wraps
from flask import abort, session
from .models.users import User


def role_required(roles):
    """
    Decorator dùng để kiểm tra vai trò của người dùng.

    :param roles: Danh sách các role_id được phép truy cập.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = session.get('user_id')

            # Kiểm tra nếu người dùng chưa đăng nhập
            if not user_id:
                return abort(401)  # Unauthorized

            # Lấy thông tin người dùng từ cơ sở dữ liệu
            user = User.query.get(user_id)

            if not user:
                return abort(401)  # Unauthorized nếu user_id không hợp lệ

            # Kiểm tra vai trò của người dùng
            if user.role_id not in roles:
                return abort(403)  # Forbidden nếu vai trò không phù hợp

            # Nếu hợp lệ, tiếp tục thực hiện hàm được bọc
            return f(*args, **kwargs)

        return decorated_function
    return decorator
