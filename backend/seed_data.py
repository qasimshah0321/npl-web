"""
Seed script to populate NPL Cricket Tournament database with NPL Season 7 data
"""
import sys
import os
import json

# Add parent directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.database import get_db_connection, init_db
from datetime import datetime, timedelta


def clear_existing_data(conn):
    """Clear existing tournament data"""
    cursor = conn.cursor()

    print("Clearing existing data...")
    cursor.execute('DELETE FROM player_statistics')
    cursor.execute('DELETE FROM matches')
    cursor.execute('DELETE FROM players')
    cursor.execute('DELETE FROM teams')
    conn.commit()
    print("Existing data cleared.")


def load_npl7_data():
    """Load NPL 7 data from JSON file"""
    json_path = os.path.join(os.path.dirname(__file__), '..', 'npl7_complete_data.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def seed_teams(conn, npl_data):
    """Seed teams data from NPL 7"""
    cursor = conn.cursor()

    teams = npl_data['teams']

    print(f"\nSeeding {len(teams)} teams...")
    team_ids = {}

    for team_name in teams:
        cursor.execute(
            '''INSERT INTO teams (name, coach_name, home_ground)
               VALUES (?, ?, ?)''',
            (team_name, 'TBD', 'TBD')
        )
        team_id = cursor.lastrowid
        team_ids[team_name] = team_id
        print(f"  [+] Added: {team_name}")

    conn.commit()
    return team_ids


def seed_players(conn, team_ids):
    """Seed players data for all teams"""
    cursor = conn.cursor()

    # Player templates (11 players per team)
    player_templates = [
        {'role': 'Batsman', 'batting_style': 'Right-hand', 'bowling_style': None},
        {'role': 'Batsman', 'batting_style': 'Left-hand', 'bowling_style': None},
        {'role': 'All-rounder', 'batting_style': 'Right-hand', 'bowling_style': 'Right-arm Fast'},
        {'role': 'All-rounder', 'batting_style': 'Right-hand', 'bowling_style': 'Right-arm Spin'},
        {'role': 'Bowler', 'batting_style': 'Right-hand', 'bowling_style': 'Right-arm Fast'},
        {'role': 'Bowler', 'batting_style': 'Right-hand', 'bowling_style': 'Left-arm Fast'},
        {'role': 'Bowler', 'batting_style': 'Left-hand', 'bowling_style': 'Right-arm Spin'},
        {'role': 'Batsman', 'batting_style': 'Right-hand', 'bowling_style': None},
        {'role': 'Wicket-keeper', 'batting_style': 'Right-hand', 'bowling_style': None},
        {'role': 'All-rounder', 'batting_style': 'Left-hand', 'bowling_style': 'Right-arm Medium'},
        {'role': 'Batsman', 'batting_style': 'Right-hand', 'bowling_style': None}
    ]

    first_names = ['Anil', 'Bikash', 'Deepak', 'Kamal', 'Manoj', 'Nabin', 'Prakash', 'Rajesh', 'Sanjay', 'Sunil', 'Ramesh']
    last_names = ['Sharma', 'Thapa', 'Gurung', 'Rai', 'Bajracharya', 'Tamang', 'Poudel', 'Chaudhary', 'Bhandari', 'Karki', 'Shrestha']

    print("\nSeeding players...")
    player_count = 0

    for idx, (team_name, team_id) in enumerate(team_ids.items()):
        print(f"  Adding players for {team_name}...")

        for jersey_num, template in enumerate(player_templates, start=1):
            player_name = f"{first_names[jersey_num - 1]} {last_names[(idx + jersey_num) % len(last_names)]}"

            cursor.execute(
                '''INSERT INTO players (name, team_id, role, jersey_number, batting_style, bowling_style)
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (player_name, team_id, template['role'], jersey_num,
                 template['batting_style'], template['bowling_style'])
            )

            player_id = cursor.lastrowid

            # Add initial statistics for each player
            cursor.execute(
                '''INSERT INTO player_statistics (player_id, matches_played, runs_scored,
                   balls_faced, fours, sixes, wickets_taken, balls_bowled, runs_conceded, catches, stumpings)
                   VALUES (?, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)''',
                (player_id,)
            )

            player_count += 1

        # Set captain (first player of each team)
        cursor.execute(
            'UPDATE teams SET captain_id = (SELECT id FROM players WHERE team_id = ? LIMIT 1) WHERE id = ?',
            (team_id, team_id)
        )

    conn.commit()
    print(f"  [+] Added {player_count} players across all teams")


def seed_matches(conn, team_ids, npl_data):
    """Seed match schedule from NPL 7 data"""
    cursor = conn.cursor()

    matches = npl_data['matches']

    print(f"\nSeeding {len(matches)} matches...")

    matches_added = 0
    for match_data in matches:
        team_a_name = match_data['team_a']
        team_b_name = match_data['team_b']

        # Get team IDs
        team_a_id = team_ids.get(team_a_name)
        team_b_id = team_ids.get(team_b_name)

        if not team_a_id or not team_b_id:
            print(f"  [!] Skipping match: {team_a_name} vs {team_b_name} (team not found)")
            continue

        # Parse date
        try:
            if isinstance(match_data['date'], str):
                match_date = datetime.strptime(match_data['date'], '%Y-%m-%d %H:%M:%S')
            else:
                match_date = match_data['date']
        except:
            match_date = datetime(2025, 11, 17)  # Default date

        # Determine round based on group
        group = match_data.get('group', 'N/A')
        round_name = f"Group {group}" if group != 'N/A' else "Group Stage"

        # Get winner ID if result exists
        winner_id = None
        result_text = match_data.get('result')
        if result_text:
            winner_id = team_ids.get(result_text)

        # Determine status
        status = 'completed' if result_text else 'scheduled'

        cursor.execute(
            '''INSERT INTO matches (match_date, match_day, team_a_id, team_b_id,
               venue, match_time, round, status, winner_id)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (match_date.strftime('%Y-%m-%d'),
             match_data.get('day', 'TBD'),
             team_a_id, team_b_id,
             'TBD', match_data.get('time', 'TBD'),
             round_name, status, winner_id)
        )
        matches_added += 1

    conn.commit()
    print(f"  [+] Added {matches_added} matches")


def update_tournament_settings(conn):
    """Update tournament settings"""
    cursor = conn.cursor()

    print("\nUpdating tournament settings...")
    cursor.execute(
        '''UPDATE tournament_settings
           SET tournament_name = ?,
               total_teams = ?,
               tournament_format = ?,
               start_date = ?,
               end_date = ?,
               is_active = 1
           WHERE id = 1''',
        ('NPL Season 7', 24, 'Group Stage + Knockout', '2025-11-17', '2025-11-30')
    )
    conn.commit()
    print("  [+] Tournament settings updated")


def main():
    """Main seeding function"""
    print("="*60)
    print("NPL Season 7 - Database Seed Script")
    print("="*60)

    # Initialize database tables first
    print("\nInitializing database tables...")
    init_db()
    print("Database tables initialized.")

    # Load NPL 7 data
    print("\nLoading NPL 7 data from Excel extraction...")
    npl_data = load_npl7_data()
    print(f"Loaded {len(npl_data['teams'])} teams and {len(npl_data['matches'])} matches")

    conn = get_db_connection()

    try:
        # Clear existing data
        clear_existing_data(conn)

        # Seed data
        team_ids = seed_teams(conn, npl_data)
        seed_players(conn, team_ids)
        seed_matches(conn, team_ids, npl_data)
        update_tournament_settings(conn)

        print("\n" + "="*60)
        print("Database seeded successfully!")
        print("="*60)
        print("\nSummary:")
        print(f"  - {len(team_ids)} Teams added")
        print(f"  - {len(team_ids) * 11} Players added (11 per team)")
        print(f"  - {len(npl_data['matches'])} Matches scheduled")
        print(f"  - Tournament: NPL Season 7")
        print(f"  - Format: Group Stage + Knockout")
        print("="*60)

    except Exception as e:
        print(f"\n[ERROR] Error seeding database: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    main()
