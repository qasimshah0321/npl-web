from flask import Blueprint, request, jsonify
from flask_login import login_required
from backend.auth import admin_required
from backend.database import execute_query, execute_single, execute_insert, execute_update, execute_delete
from datetime import datetime

matches_bp = Blueprint('matches', __name__, url_prefix='/api/matches')


@matches_bp.route('', methods=['GET'])
def get_matches():
    """Get all matches"""
    matches = execute_query('''
        SELECT m.*,
               ta.name as team_a_name, ta.logo_path as team_a_logo,
               tb.name as team_b_name, tb.logo_path as team_b_logo,
               w.name as winner_name
        FROM matches m
        JOIN teams ta ON m.team_a_id = ta.id
        JOIN teams tb ON m.team_b_id = tb.id
        LEFT JOIN teams w ON m.winner_id = w.id
        ORDER BY m.match_date ASC, m.match_time ASC
    ''')
    return jsonify(matches), 200


@matches_bp.route('/<int:match_id>', methods=['GET'])
def get_match(match_id):
    """Get single match details"""
    match = execute_single('''
        SELECT m.*,
               ta.name as team_a_name, ta.logo_path as team_a_logo,
               tb.name as team_b_name, tb.logo_path as team_b_logo,
               w.name as winner_name
        FROM matches m
        JOIN teams ta ON m.team_a_id = ta.id
        JOIN teams tb ON m.team_b_id = tb.id
        LEFT JOIN teams w ON m.winner_id = w.id
        WHERE m.id = ?
    ''', (match_id,))

    if not match:
        return jsonify({'error': 'Match not found'}), 404

    return jsonify(match), 200


@matches_bp.route('/round/<string:round_name>', methods=['GET'])
def get_matches_by_round(round_name):
    """Get matches by round"""
    matches = execute_query('''
        SELECT m.*,
               ta.name as team_a_name, ta.logo_path as team_a_logo,
               tb.name as team_b_name, tb.logo_path as team_b_logo,
               w.name as winner_name
        FROM matches m
        JOIN teams ta ON m.team_a_id = ta.id
        JOIN teams tb ON m.team_b_id = tb.id
        LEFT JOIN teams w ON m.winner_id = w.id
        WHERE m.round = ?
        ORDER BY m.match_date ASC, m.match_time ASC
    ''', (round_name,))

    return jsonify(matches), 200


@matches_bp.route('', methods=['POST'])
@admin_required
def create_match():
    """Create new match (admin only)"""
    data = request.get_json()

    required_fields = ['match_date', 'match_day', 'team_a_id', 'team_b_id', 'round']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        match_id = execute_insert('''
            INSERT INTO matches
            (match_date, match_day, team_a_id, team_b_id, venue, match_time, round, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['match_date'],
            data['match_day'],
            data['team_a_id'],
            data['team_b_id'],
            data.get('venue'),
            data.get('match_time'),
            data['round'],
            data.get('status', 'scheduled')
        ))

        return jsonify({
            'message': 'Match created successfully',
            'match_id': match_id
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@matches_bp.route('/<int:match_id>', methods=['PUT'])
@admin_required
def update_match(match_id):
    """Update match (admin only)"""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        affected = execute_update('''
            UPDATE matches
            SET match_date = ?, match_day = ?, team_a_id = ?, team_b_id = ?,
                venue = ?, match_time = ?, round = ?, status = ?
            WHERE id = ?
        ''', (
            data.get('match_date'),
            data.get('match_day'),
            data.get('team_a_id'),
            data.get('team_b_id'),
            data.get('venue'),
            data.get('match_time'),
            data.get('round'),
            data.get('status'),
            match_id
        ))

        if affected == 0:
            return jsonify({'error': 'Match not found'}), 404

        return jsonify({'message': 'Match updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@matches_bp.route('/<int:match_id>/result', methods=['PUT'])
@admin_required
def update_result(match_id):
    """Update match result (admin only)"""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        affected = execute_update('''
            UPDATE matches
            SET winner_id = ?, team_a_score = ?, team_b_score = ?,
                result_summary = ?, status = ?
            WHERE id = ?
        ''', (
            data.get('winner_id'),
            data.get('team_a_score'),
            data.get('team_b_score'),
            data.get('result_summary'),
            'completed',
            match_id
        ))

        if affected == 0:
            return jsonify({'error': 'Match not found'}), 404

        return jsonify({'message': 'Match result updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@matches_bp.route('/<int:match_id>', methods=['DELETE'])
@admin_required
def delete_match(match_id):
    """Delete match (admin only)"""
    try:
        affected = execute_delete('DELETE FROM matches WHERE id = ?', (match_id,))

        if affected == 0:
            return jsonify({'error': 'Match not found'}), 404

        return jsonify({'message': 'Match deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
