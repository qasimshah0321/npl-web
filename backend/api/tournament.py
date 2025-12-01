from flask import Blueprint, request, jsonify
from flask_login import login_required
from backend.auth import admin_required
from backend.database import execute_query, execute_single, execute_update, execute_insert
from datetime import datetime, timedelta

tournament_bp = Blueprint('tournament', __name__, url_prefix='/api/tournament')


@tournament_bp.route('/settings', methods=['GET'])
def get_settings():
    """Get tournament settings"""
    settings = execute_single(
        'SELECT * FROM tournament_settings WHERE is_active = 1 ORDER BY id DESC LIMIT 1'
    )

    if not settings:
        return jsonify({'error': 'No active tournament found'}), 404

    return jsonify(settings), 200


@tournament_bp.route('/settings', methods=['PUT'])
@admin_required
def update_settings():
    """Update tournament settings (admin only)"""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Get current active tournament
    current = execute_single(
        'SELECT id FROM tournament_settings WHERE is_active = 1 ORDER BY id DESC LIMIT 1'
    )

    if not current:
        return jsonify({'error': 'No active tournament found'}), 404

    try:
        affected = execute_update('''
            UPDATE tournament_settings
            SET tournament_name = ?, total_teams = ?, tournament_format = ?,
                start_date = ?, end_date = ?
            WHERE id = ?
        ''', (
            data.get('tournament_name'),
            data.get('total_teams'),
            data.get('tournament_format'),
            data.get('start_date'),
            data.get('end_date'),
            current['id']
        ))

        return jsonify({'message': 'Tournament settings updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@tournament_bp.route('/bracket', methods=['GET'])
def get_bracket():
    """Get tournament bracket structure"""
    matches = execute_query('''
        SELECT m.*,
               ta.name as team_a_name, ta.logo_path as team_a_logo,
               tb.name as team_b_name, tb.logo_path as team_b_logo,
               w.name as winner_name
        FROM matches m
        JOIN teams ta ON m.team_a_id = ta.id
        JOIN teams tb ON m.team_b_id = tb.id
        LEFT JOIN teams w ON m.winner_id = w.id
        ORDER BY
            CASE m.round
                WHEN 'Final' THEN 4
                WHEN 'Semi-Final' THEN 3
                WHEN 'Round 2' THEN 2
                WHEN 'Round 1' THEN 1
                ELSE 0
            END,
            m.match_date, m.match_time
    ''')

    # Organize matches by round
    bracket = {
        'Round 1': [],
        'Round 2': [],
        'Semi-Final': [],
        'Final': []
    }

    for match in matches:
        round_name = match['round']
        if round_name in bracket:
            bracket[round_name].append(match)

    return jsonify(bracket), 200


@tournament_bp.route('/generate', methods=['POST'])
@admin_required
def generate_bracket():
    """Auto-generate tournament bracket (admin only)"""
    data = request.get_json()

    if not data or not data.get('start_date'):
        return jsonify({'error': 'Start date required'}), 400

    # Get all teams
    teams = execute_query('SELECT id, name FROM teams ORDER BY RANDOM()')
    team_count = len(teams)

    if team_count < 2:
        return jsonify({'error': 'At least 2 teams required'}), 400

    try:
        # Determine tournament structure based on team count
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        match_day_offset = 0

        # Delete existing matches if requested
        if data.get('clear_existing'):
            execute_query('DELETE FROM matches')

        # Generate matches based on team count
        if team_count <= 4:
            # Semi-finals only
            rounds = [('Semi-Final', 2)]
        elif team_count <= 8:
            # Quarter-finals + Semi-finals
            rounds = [('Round 1', 4), ('Semi-Final', 2)]
        elif team_count <= 16:
            # Round 1, Round 2, Semi-finals
            rounds = [('Round 1', 8), ('Round 2', 4), ('Semi-Final', 2)]
        else:
            # For more teams, create multiple preliminary rounds
            rounds = [('Round 1', 16), ('Round 2', 8), ('Semi-Final', 2)]

        # Generate Round 1 matches
        team_index = 0
        for round_name, match_count in rounds:
            if round_name == 'Round 1':
                for i in range(match_count):
                    if team_index + 1 < len(teams):
                        match_date = start_date + timedelta(days=match_day_offset)
                        day_name = match_date.strftime('%A')

                        execute_insert('''
                            INSERT INTO matches
                            (match_date, match_day, team_a_id, team_b_id, round, venue, match_time, status)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            match_date.strftime('%Y-%m-%d'),
                            day_name,
                            teams[team_index]['id'],
                            teams[team_index + 1]['id'],
                            round_name,
                            data.get('venue', 'TBD'),
                            data.get('match_time', '14:00'),
                            'scheduled'
                        ))

                        team_index += 2
                        match_day_offset += 1

        # Create placeholder matches for later rounds
        match_day_offset += 2  # Gap between rounds

        for round_name, match_count in rounds[1:]:
            for i in range(match_count):
                match_date = start_date + timedelta(days=match_day_offset)
                day_name = match_date.strftime('%A')

                # Create placeholder matches (teams TBD)
                # For now, use first two teams as placeholders
                execute_insert('''
                    INSERT INTO matches
                    (match_date, match_day, team_a_id, team_b_id, round, venue, match_time, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    match_date.strftime('%Y-%m-%d'),
                    day_name,
                    teams[0]['id'],  # Placeholder
                    teams[1]['id'],  # Placeholder
                    round_name,
                    data.get('venue', 'TBD'),
                    data.get('match_time', '14:00'),
                    'scheduled'
                ))

                match_day_offset += 1

        # Create Final match
        match_day_offset += 3
        final_date = start_date + timedelta(days=match_day_offset)
        execute_insert('''
            INSERT INTO matches
            (match_date, match_day, team_a_id, team_b_id, round, venue, match_time, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            final_date.strftime('%Y-%m-%d'),
            final_date.strftime('%A'),
            teams[0]['id'],  # Placeholder
            teams[1]['id'],  # Placeholder
            'Final',
            data.get('venue', 'TBD'),
            data.get('match_time', '18:00'),
            'scheduled'
        ))

        return jsonify({
            'message': 'Tournament bracket generated successfully',
            'teams_count': team_count
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
