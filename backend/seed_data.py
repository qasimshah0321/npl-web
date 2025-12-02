"""
Seed script to populate NPL Cricket Tournament database with initial data
"""
import sys
import os

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


def seed_teams(conn):
    """Seed teams data"""
    cursor = conn.cursor()

    teams = [
        {
            'name': 'Kathmandu Kings XI',
            'coach_name': 'Rajesh Sharma',
            'home_ground': 'TU Cricket Ground, Kirtipur'
        },
        {
            'name': 'Pokhara Rhinos',
            'coach_name': 'Binod Thapa',
            'home_ground': 'Pokhara Rangasala'
        },
        {
            'name': 'Chitwan Tigers',
            'coach_name': 'Sanjay Gurung',
            'home_ground': 'Chitwan Cricket Stadium'
        },
        {
            'name': 'Biratnagar Warriors',
            'coach_name': 'Dinesh Rai',
            'home_ground': 'Biratnagar Sports Complex'
        },
        {
            'name': 'Lalitpur Patriots',
            'coach_name': 'Kiran Bajracharya',
            'home_ground': 'Satdobato Cricket Ground'
        },
        {
            'name': 'Bhaktapur Legends',
            'coach_name': 'Prakash Tamang',
            'home_ground': 'Bhaktapur Sports Arena'
        },
        {
            'name': 'Butwal Blasters',
            'coach_name': 'Ramesh Poudel',
            'home_ground': 'Butwal Stadium'
        },
        {
            'name': 'Dhangadhi Thunders',
            'coach_name': 'Anil Chaudhary',
            'home_ground': 'Dhangadhi Cricket Ground'
        }
    ]

    print("\nSeeding teams...")
    team_ids = []
    for team in teams:
        cursor.execute(
            '''INSERT INTO teams (name, coach_name, home_ground)
               VALUES (?, ?, ?)''',
            (team['name'], team['coach_name'], team['home_ground'])
        )
        team_ids.append(cursor.lastrowid)
        print(f"  [+] Added: {team['name']}")

    conn.commit()
    return team_ids


def seed_players(conn, team_ids):
    """Seed players data for all teams"""
    cursor = conn.cursor()

    # Sample players for each team (11 players per team)
    batting_styles = ['Right-hand', 'Left-hand']
    bowling_styles = ['Right-arm Fast', 'Left-arm Fast', 'Right-arm Spin', 'Left-arm Spin', 'Right-arm Medium']
    roles = ['Batsman', 'Bowler', 'All-rounder', 'Wicket-keeper']

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

    for idx, team_id in enumerate(team_ids):
        cursor.execute('SELECT name FROM teams WHERE id = ?', (team_id,))
        team_name = cursor.fetchone()[0]
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


def seed_matches(conn, team_ids):
    """Seed match schedule"""
    cursor = conn.cursor()

    # Quarter-finals schedule (8 teams, 4 matches)
    base_date = datetime(2024, 12, 15)

    print("\nSeeding matches...")

    # Quarter-finals
    quarter_finals = [
        {
            'team_a': team_ids[0],  # Kathmandu Kings XI
            'team_b': team_ids[1],  # Pokhara Rhinos
            'venue': 'TU Cricket Ground, Kirtipur',
            'date': base_date,
            'time': '10:00 AM'
        },
        {
            'team_a': team_ids[2],  # Chitwan Tigers
            'team_b': team_ids[3],  # Biratnagar Warriors
            'venue': 'TU Cricket Ground, Kirtipur',
            'time': '02:00 PM',
            'date': base_date
        },
        {
            'team_a': team_ids[4],  # Lalitpur Patriots
            'team_b': team_ids[5],  # Bhaktapur Legends
            'venue': 'Satdobato Cricket Ground',
            'date': base_date + timedelta(days=1),
            'time': '10:00 AM'
        },
        {
            'team_a': team_ids[6],  # Butwal Blasters
            'team_b': team_ids[7],  # Dhangadhi Thunders
            'venue': 'Satdobato Cricket Ground',
            'date': base_date + timedelta(days=1),
            'time': '02:00 PM'
        }
    ]

    for match in quarter_finals:
        cursor.execute(
            '''INSERT INTO matches (match_date, match_day, team_a_id, team_b_id,
               venue, match_time, round, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (match['date'].strftime('%Y-%m-%d'),
             match['date'].strftime('%A'),
             match['team_a'], match['team_b'],
             match['venue'], match['time'],
             'Quarter-final', 'scheduled')
        )

    print(f"  [+] Added 4 Quarter-final matches")

    # Semi-finals (TBD teams)
    semi_final_date = base_date + timedelta(days=3)
    semi_finals = [
        {
            'venue': 'TU Cricket Ground, Kirtipur',
            'date': semi_final_date,
            'time': '10:00 AM'
        },
        {
            'venue': 'TU Cricket Ground, Kirtipur',
            'date': semi_final_date,
            'time': '02:00 PM'
        }
    ]

    # For semi-finals, we'll use placeholder teams (first 4 teams)
    for idx, match in enumerate(semi_finals):
        cursor.execute(
            '''INSERT INTO matches (match_date, match_day, team_a_id, team_b_id,
               venue, match_time, round, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (match['date'].strftime('%Y-%m-%d'),
             match['date'].strftime('%A'),
             team_ids[idx * 2], team_ids[idx * 2 + 1],
             match['venue'], match['time'],
             'Semi-final', 'scheduled')
        )

    print(f"  [+] Added 2 Semi-final matches")

    # Final
    final_date = base_date + timedelta(days=5)
    cursor.execute(
        '''INSERT INTO matches (match_date, match_day, team_a_id, team_b_id,
           venue, match_time, round, status)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (final_date.strftime('%Y-%m-%d'),
         final_date.strftime('%A'),
         team_ids[0], team_ids[1],
         'TU Cricket Ground, Kirtipur',
         '02:00 PM',
         'Final', 'scheduled')
    )

    print(f"  [+] Added 1 Final match")

    conn.commit()
    print(f"\nTotal matches created: 7")


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
        ('NPL Cricket Tournament 2024', 8, 'Knockout', '2024-12-15', '2024-12-20')
    )
    conn.commit()
    print("  [+] Tournament settings updated")


def main():
    """Main seeding function"""
    print("="*60)
    print("NPL Cricket Tournament - Database Seed Script")
    print("="*60)

    # Initialize database tables first
    print("\nInitializing database tables...")
    init_db()
    print("Database tables initialized.")

    conn = get_db_connection()

    try:
        # Clear existing data
        clear_existing_data(conn)

        # Seed data
        team_ids = seed_teams(conn)
        seed_players(conn, team_ids)
        seed_matches(conn, team_ids)
        update_tournament_settings(conn)

        print("\n" + "="*60)
        print("Database seeded successfully!")
        print("="*60)
        print("\nSummary:")
        print(f"  - 8 Teams added")
        print(f"  - 88 Players added (11 per team)")
        print(f"  - 7 Matches scheduled (4 QF, 2 SF, 1 Final)")
        print(f"  - Tournament: NPL Cricket Tournament 2024")
        print(f"  - Format: Knockout")
        print("="*60)

    except Exception as e:
        print(f"\n[ERROR] Error seeding database: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    main()
