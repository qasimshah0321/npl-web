from werkzeug.security import check_password_hash
from backend.database import execute_single


class User:
    """User model for authentication"""

    def __init__(self, id, username, password_hash, role, created_at):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.created_at = created_at
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        """Return user ID as string for Flask-Login"""
        return str(self.id)

    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        """Check if user has admin role"""
        return self.role == 'admin'

    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        user_data = execute_single(
            'SELECT * FROM users WHERE id = ?',
            (user_id,)
        )
        if user_data:
            return User(**user_data)
        return None

    @staticmethod
    def get_by_username(username):
        """Get user by username"""
        user_data = execute_single(
            'SELECT * FROM users WHERE username = ?',
            (username,)
        )
        if user_data:
            return User(**user_data)
        return None

    def to_dict(self):
        """Convert user to dictionary (excluding password)"""
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'created_at': self.created_at
        }
