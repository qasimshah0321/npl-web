import sys
import os

# Add parent directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, send_from_directory, jsonify
from flask_login import LoginManager
from flask_cors import CORS
from backend.config import Config
from backend.database import init_db
from backend.models import User
from backend.auth import auth_bp
from backend.api.teams import teams_bp
from backend.api.players import players_bp
from backend.api.matches import matches_bp
from backend.api.tournament import tournament_bp


def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__,
                static_folder='../frontend',
                static_url_path='')

    # Load configuration
    app.config.from_object(Config)
    Config.init_app(app)

    # Initialize CORS
    CORS(app, supports_credentials=True)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(int(user_id))

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(teams_bp)
    app.register_blueprint(players_bp)
    app.register_blueprint(matches_bp)
    app.register_blueprint(tournament_bp)

    # Serve frontend pages
    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/<path:path>')
    def serve_static(path):
        if os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    # Serve uploaded files
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(Config.UPLOAD_FOLDER, filename)

    # Health check endpoint
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy'}), 200

    # Initialize database
    with app.app_context():
        init_db()

    return app


if __name__ == '__main__':
    app = create_app()

    # Get port from environment variable or use 5000
    port = int(os.environ.get('PORT', 5000))

    print("\n" + "="*50)
    print("NPL Cricket Tournament Management System")
    print("="*50)
    print(f"Server running at: http://localhost:{port}")
    print("Default admin credentials:")
    print("  Username: admin")
    print("  Password: admin123")
    print("="*50 + "\n")

    # Use debug=False in production
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)
