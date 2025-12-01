from flask import Blueprint, request, jsonify
from flask_login import login_required
from werkzeug.utils import secure_filename
import os
import time
from backend.auth import admin_required
from backend.database import execute_query, execute_single, execute_insert, execute_update, execute_delete
from backend.config import Config

teams_bp = Blueprint('teams', __name__, url_prefix='/api/teams')


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


@teams_bp.route('', methods=['GET'])
def get_teams():
    """Get all teams"""
    teams = execute_query('''
        SELECT t.*, p.name as captain_name,
               (SELECT COUNT(*) FROM players WHERE team_id = t.id) as player_count
        FROM teams t
        LEFT JOIN players p ON t.captain_id = p.id
        ORDER BY t.created_at DESC
    ''')
    return jsonify(teams), 200


@teams_bp.route('/<int:team_id>', methods=['GET'])
def get_team(team_id):
    """Get single team with details"""
    team = execute_single('''
        SELECT t.*, p.name as captain_name
        FROM teams t
        LEFT JOIN players p ON t.captain_id = p.id
        WHERE t.id = ?
    ''', (team_id,))

    if not team:
        return jsonify({'error': 'Team not found'}), 404

    # Get team players
    players = execute_query(
        'SELECT * FROM players WHERE team_id = ? ORDER BY jersey_number',
        (team_id,)
    )

    team['players'] = players
    return jsonify(team), 200


@teams_bp.route('', methods=['POST'])
@admin_required
def create_team():
    """Create new team (admin only)"""
    data = request.get_json()

    if not data or not data.get('name'):
        return jsonify({'error': 'Team name is required'}), 400

    try:
        team_id = execute_insert('''
            INSERT INTO teams (name, coach_name, home_ground)
            VALUES (?, ?, ?)
        ''', (
            data['name'],
            data.get('coach_name'),
            data.get('home_ground')
        ))

        return jsonify({
            'message': 'Team created successfully',
            'team_id': team_id
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@teams_bp.route('/<int:team_id>', methods=['PUT'])
@admin_required
def update_team(team_id):
    """Update team (admin only)"""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        affected = execute_update('''
            UPDATE teams
            SET name = ?, coach_name = ?, home_ground = ?, captain_id = ?
            WHERE id = ?
        ''', (
            data.get('name'),
            data.get('coach_name'),
            data.get('home_ground'),
            data.get('captain_id'),
            team_id
        ))

        if affected == 0:
            return jsonify({'error': 'Team not found'}), 404

        return jsonify({'message': 'Team updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@teams_bp.route('/<int:team_id>', methods=['DELETE'])
@admin_required
def delete_team(team_id):
    """Delete team (admin only)"""
    try:
        affected = execute_delete('DELETE FROM teams WHERE id = ?', (team_id,))

        if affected == 0:
            return jsonify({'error': 'Team not found'}), 404

        return jsonify({'message': 'Team deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@teams_bp.route('/<int:team_id>/logo', methods=['POST'])
@admin_required
def upload_logo(team_id):
    """Upload team logo (admin only)"""
    if 'logo' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['logo']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    try:
        # Create unique filename
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{team_id}_{int(time.time())}.{ext}"
        filepath = os.path.join(Config.TEAM_UPLOAD_FOLDER, unique_filename)

        # Save file
        file.save(filepath)

        # Update database
        logo_path = f"uploads/teams/{unique_filename}"
        execute_update(
            'UPDATE teams SET logo_path = ? WHERE id = ?',
            (logo_path, team_id)
        )

        return jsonify({
            'message': 'Logo uploaded successfully',
            'logo_path': logo_path
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
