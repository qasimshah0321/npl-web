# Database Seeding Instructions

This document explains how to populate the NPL Cricket Tournament database with initial data.

## Overview

The seed script (`backend/seed_data.py`) populates the database with:
- 8 Teams with coaches and home grounds
- 88 Players (11 players per team) with roles and statistics
- 7 Matches (4 Quarter-finals, 2 Semi-finals, 1 Final)
- Tournament settings

## How to Run the Seed Script

### Windows:
```bash
venv\Scripts\python.exe backend\seed_data.py
```

### Linux/Mac:
```bash
venv/bin/python backend/seed_data.py
```

## What the Script Does

1. **Clears existing tournament data** - Removes all teams, players, matches, and statistics
2. **Seeds teams** - Creates 8 teams:
   - Kathmandu Kings XI
   - Pokhara Rhinos
   - Chitwan Tigers
   - Biratnagar Warriors
   - Lalitpur Patriots
   - Bhaktapur Legends
   - Butwal Blasters
   - Dhangadhi Thunders

3. **Seeds players** - Creates 11 players per team with:
   - Jersey numbers (1-11)
   - Roles (Batsman, Bowler, All-rounder, Wicket-keeper)
   - Batting and bowling styles
   - Initial statistics (all zeros)

4. **Seeds matches** - Creates knockout tournament schedule:
   - Quarter-finals: Dec 15-16, 2024
   - Semi-finals: Dec 18, 2024
   - Final: Dec 20, 2024

5. **Updates tournament settings** - Sets tournament name, format, and dates

## Important Notes

- The script will DELETE all existing tournament data before seeding
- Admin user and authentication data are preserved
- The script is safe to run multiple times
- All matches are initially set to "scheduled" status
- Player statistics start at zero and will be updated as matches are played

## Verify the Data

After running the seed script, start the server:
```bash
venv\Scripts\python.exe backend\app.py
```

Then test the API endpoints:
- Teams: http://localhost:5000/api/teams
- Matches: http://localhost:5000/api/matches
- Players: http://localhost:5000/api/players

## Customizing the Data

To modify the seed data:
1. Edit `backend/seed_data.py`
2. Update the teams, players, or matches data structures
3. Run the script again to apply changes

## Database Location

The SQLite database is located at:
```
database/cricket.db
```
