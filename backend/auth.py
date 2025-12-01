from flask import Blueprint, request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from backend.models import User
from backend.database import execute_insert, execute_query
from functools import wraps

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400

    user = User.get_by_username(data['username'])

    if user and user.check_password(data['password']):
        login_user(user, remember=data.get('remember', False))
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict()
        }), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """User logout endpoint"""
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200


@auth_bp.route('/check', methods=['GET'])
def check_auth():
    """Check authentication status"""
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': current_user.to_dict()
        }), 200
    else:
        return jsonify({'authenticated': False}), 200


@auth_bp.route('/register', methods=['POST'])
@admin_required
def register():
    """Register new user (admin only)"""
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400

    # Check if user already exists
    existing_user = User.get_by_username(data['username'])
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 400

    role = data.get('role', 'viewer')
    if role not in ['admin', 'viewer']:
        return jsonify({'error': 'Invalid role'}), 400

    password_hash = generate_password_hash(data['password'])

    try:
        user_id = execute_insert(
            'INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
            (data['username'], password_hash, role)
        )
        return jsonify({
            'message': 'User created successfully',
            'user_id': user_id
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
