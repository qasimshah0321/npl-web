import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash
from backend.config import Config


def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database with tables"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'viewer',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create teams table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            logo_path TEXT,
            captain_id INTEGER,
            coach_name TEXT,
            home_ground TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (captain_id) REFERENCES players(id)
        )
    ''')

    # Create players table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            team_id INTEGER NOT NULL,
            photo_path TEXT,
            role TEXT NOT NULL,
            jersey_number INTEGER,
            batting_style TEXT,
            bowling_style TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE
        )
    ''')

    # Create player_statistics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS player_statistics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER NOT NULL,
            matches_played INTEGER DEFAULT 0,
            runs_scored INTEGER DEFAULT 0,
            balls_faced INTEGER DEFAULT 0,
            fours INTEGER DEFAULT 0,
            sixes INTEGER DEFAULT 0,
            wickets_taken INTEGER DEFAULT 0,
            balls_bowled INTEGER DEFAULT 0,
            runs_conceded INTEGER DEFAULT 0,
            catches INTEGER DEFAULT 0,
            stumpings INTEGER DEFAULT 0,
            FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE CASCADE
        )
    ''')

    # Create matches table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_date DATE NOT NULL,
            match_day TEXT NOT NULL,
            team_a_id INTEGER NOT NULL,
            team_b_id INTEGER NOT NULL,
            venue TEXT,
            match_time TEXT,
            round TEXT NOT NULL,
            status TEXT DEFAULT 'scheduled',
            winner_id INTEGER,
            team_a_score TEXT,
            team_b_score TEXT,
            result_summary TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (team_a_id) REFERENCES teams(id),
            FOREIGN KEY (team_b_id) REFERENCES teams(id),
            FOREIGN KEY (winner_id) REFERENCES teams(id)
        )
    ''')

    # Create tournament_settings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tournament_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tournament_name TEXT NOT NULL,
            total_teams INTEGER NOT NULL,
            tournament_format TEXT,
            start_date DATE,
            end_date DATE,
            is_active BOOLEAN DEFAULT 1
        )
    ''')

    conn.commit()

    # Create default admin user if none exists
    cursor.execute('SELECT COUNT(*) FROM users WHERE role = ?', ('admin',))
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            'INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
            ('admin', generate_password_hash('admin123'), 'admin')
        )
        conn.commit()
        print("Default admin user created (username: admin, password: admin123)")

    # Create default tournament settings if none exist
    cursor.execute('SELECT COUNT(*) FROM tournament_settings')
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            '''INSERT INTO tournament_settings
               (tournament_name, total_teams, tournament_format, is_active)
               VALUES (?, ?, ?, ?)''',
            ('NPL Cricket Tournament 2024', 8, 'knockout', 1)
        )
        conn.commit()
        print("Default tournament settings created")

    conn.close()
    print("Database initialized successfully")


def dict_from_row(row):
    """Convert a sqlite3.Row object to a dictionary"""
    return dict(zip(row.keys(), row)) if row else None


def execute_query(query, params=()):
    """Execute a query and return results"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return [dict_from_row(row) for row in results]


def execute_single(query, params=()):
    """Execute a query and return a single result"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchone()
    conn.close()
    return dict_from_row(result)


def execute_insert(query, params=()):
    """Execute an insert query and return the last row id"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    last_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return last_id


def execute_update(query, params=()):
    """Execute an update query"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    affected_rows = cursor.rowcount
    conn.close()
    return affected_rows


def execute_delete(query, params=()):
    """Execute a delete query"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    affected_rows = cursor.rowcount
    conn.close()
    return affected_rows
