from flask import Blueprint, request, jsonify
from flask_login import login_required
from werkzeug.utils import secure_filename
import os
import time
from backend.auth import admin_required
from backend.database import execute_query, execute_single, execute_insert, execute_update, execute_delete
from backend.config import Config

players_bp = Blueprint('players', __name__, url_prefix='/api/players')


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


@players_bp.route('', methods=['GET'])
def get_players():
    """Get all players"""
    players = execute_query('''
        SELECT p.*, t.name as team_name,
               ps.matches_played, ps.runs_scored, ps.wickets_taken,
               ps.fours, ps.sixes, ps.catches
        FROM players p
        JOIN teams t ON p.team_id = t.id
        LEFT JOIN player_statistics ps ON p.id = ps.player_id
        ORDER BY p.created_at DESC
    ''')
    return jsonify(players), 200


@players_bp.route('/<int:player_id>', methods=['GET'])
def get_player(player_id):
    """Get single player with full statistics"""
    player = execute_single('''
        SELECT p.*, t.name as team_name,
               ps.*
        FROM players p
        JOIN teams t ON p.team_id = t.id
        LEFT JOIN player_statistics ps ON p.id = ps.player_id
        WHERE p.id = ?
    ''', (player_id,))

    if not player:
        return jsonify({'error': 'Player not found'}), 404

    return jsonify(player), 200


@players_bp.route('/team/<int:team_id>', methods=['GET'])
def get_team_players(team_id):
    """Get all players for a specific team"""
    players = execute_query('''
        SELECT p.*, ps.matches_played, ps.runs_scored, ps.wickets_taken
        FROM players p
        LEFT JOIN player_statistics ps ON p.id = ps.player_id
        WHERE p.team_id = ?
        ORDER BY p.jersey_number
    ''', (team_id,))

    return jsonify(players), 200


@players_bp.route('', methods=['POST'])
@admin_required
def create_player():
    """Create new player (admin only)"""
    data = request.get_json()

    if not data or not data.get('name') or not data.get('team_id') or not data.get('role'):
        return jsonify({'error': 'Name, team_id, and role are required'}), 400

    try:
        player_id = execute_insert('''
            INSERT INTO players (name, team_id, role, jersey_number, batting_style, bowling_style)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data['team_id'],
            data['role'],
            data.get('jersey_number'),
            data.get('batting_style'),
            data.get('bowling_style')
        ))

        # Create initial statistics record
        execute_insert(
            'INSERT INTO player_statistics (player_id) VALUES (?)',
            (player_id,)
        )

        return jsonify({
            'message': 'Player created successfully',
            'player_id': player_id
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@players_bp.route('/<int:player_id>', methods=['PUT'])
@admin_required
def update_player(player_id):
    """Update player (admin only)"""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        affected = execute_update('''
            UPDATE players
            SET name = ?, team_id = ?, role = ?, jersey_number = ?,
                batting_style = ?, bowling_style = ?
            WHERE id = ?
        ''', (
            data.get('name'),
            data.get('team_id'),
            data.get('role'),
            data.get('jersey_number'),
            data.get('batting_style'),
            data.get('bowling_style'),
            player_id
        ))

        if affected == 0:
            return jsonify({'error': 'Player not found'}), 404

        return jsonify({'message': 'Player updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@players_bp.route('/<int:player_id>', methods=['DELETE'])
@admin_required
def delete_player(player_id):
    """Delete player (admin only)"""
    try:
        affected = execute_delete('DELETE FROM players WHERE id = ?', (player_id,))

        if affected == 0:
            return jsonify({'error': 'Player not found'}), 404

        return jsonify({'message': 'Player deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@players_bp.route('/<int:player_id>/photo', methods=['POST'])
@admin_required
def upload_photo(player_id):
    """Upload player photo (admin only)"""
    if 'photo' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['photo']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    try:
        # Create unique filename
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{player_id}_{int(time.time())}.{ext}"
        filepath = os.path.join(Config.PLAYER_UPLOAD_FOLDER, unique_filename)

        # Save file
        file.save(filepath)

        # Update database
        photo_path = f"uploads/players/{unique_filename}"
        execute_update(
            'UPDATE players SET photo_path = ? WHERE id = ?',
            (photo_path, player_id)
        )

        return jsonify({
            'message': 'Photo uploaded successfully',
            'photo_path': photo_path
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@players_bp.route('/<int:player_id>/stats', methods=['PUT'])
@admin_required
def update_stats(player_id):
    """Update player statistics (admin only)"""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        affected = execute_update('''
            UPDATE player_statistics
            SET matches_played = ?, runs_scored = ?, balls_faced = ?,
                fours = ?, sixes = ?, wickets_taken = ?, balls_bowled = ?,
                runs_conceded = ?, catches = ?, stumpings = ?
            WHERE player_id = ?
        ''', (
            data.get('matches_played', 0),
            data.get('runs_scored', 0),
            data.get('balls_faced', 0),
            data.get('fours', 0),
            data.get('sixes', 0),
            data.get('wickets_taken', 0),
            data.get('balls_bowled', 0),
            data.get('runs_conceded', 0),
            data.get('catches', 0),
            data.get('stumpings', 0),
            player_id
        ))

        if affected == 0:
            return jsonify({'error': 'Player statistics not found'}), 404

        return jsonify({'message': 'Statistics updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
