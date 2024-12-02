from flask import Flask
from website.db import db  # Import db từ db.py
from .routes.routes import main_bp
from .routes.employee import employee_bp
from .routes.department import department_bp
from .routes.user import user_bp
from .routes.attendance import attendance_bp
from .auth import auth_bp


def create_app():
    app = Flask(__name__)

    # Load cấu hình
    app.config.from_object('config.Config')
    # Khởi tạo db với ứng dụng
    db.init_app(app)

    # Đăng ký các Blueprints
    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(employee_bp, url_prefix='/employees')
    app.register_blueprint(department_bp, url_prefix='/departments')
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(attendance_bp, url_prefix='/attendances')

    return app
