# Quick Start Guide - NPL Cricket Tournament

## Starting the Application

### 1. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 2. Run the Application

```bash
python backend/app.py
```

The server will start at: **http://localhost:5000**

## Default Admin Credentials

- **Username:** admin
- **Password:** admin123

## Quick Navigation

### Public Pages
- **Home:** http://localhost:5000/
- **Schedule:** http://localhost:5000/schedule.html
- **Teams:** http://localhost:5000/teams.html
- **Players:** http://localhost:5000/players.html
- **Bracket:** http://localhost:5000/bracket.html

### Admin Pages
- **Login:** http://localhost:5000/login.html
- **Admin Dashboard:** http://localhost:5000/admin.html

## Getting Started as Admin

1. Go to http://localhost:5000/login.html
2. Login with username: `admin`, password: `admin123`
3. You'll be redirected to the admin dashboard

### Add Your First Team

1. Click on "Teams" tab in admin dashboard
2. Click "Add New Team" button
3. Fill in:
   - Team Name (required)
   - Coach Name
   - Home Ground
   - Upload team logo (optional)
4. Click "Save Team"

### Add Players

1. Click on "Players" tab
2. Click "Add New Player"
3. Fill in:
   - Player Name (required)
   - Select Team (required)
   - Role: Batsman/Bowler/All-Rounder/Wicket-Keeper (required)
   - Jersey Number
   - Batting Style
   - Bowling Style
4. Click "Save Player"

### Schedule Matches

1. Click on "Matches" tab
2. Click "Add New Match"
3. Fill in:
   - Match Date (required)
   - Match Time
   - Team A (required)
   - Team B (required)
   - Venue
   - Round: Round 1/Round 2/Semi-Final/Final (required)
4. Click "Save Match"

### Update Match Results

1. Go to "Matches" tab
2. Click "Result" button for any match
3. Fill in:
   - Winner (required)
   - Team A Score (e.g., "185/7 (20)")
   - Team B Score (e.g., "160/9 (20)")
   - Result Summary (e.g., "Team A won by 25 runs")
4. Click "Update Result"

## Features Checklist

- ✅ Cricket-themed green and red design
- ✅ Match results with winning teams in GREEN
- ✅ Team and player management with photo/logo upload
- ✅ Player statistics tracking
- ✅ Tournament bracket visualization
- ✅ Flexible round structure (Round 1, Round 2, Semi-Finals, Finals)
- ✅ Admin authentication and role-based access
- ✅ Responsive design for mobile and desktop

## Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

## Troubleshooting

### Port Already in Use
If you get an error that port 5000 is already in use:
1. Find and stop the process using port 5000, OR
2. Change the port in `backend/app.py` (last line)

### Database Issues
If you need to reset the database:
1. Stop the server
2. Delete `database/cricket.db`
3. Restart the server (database will be recreated)

### Images Not Showing
Make sure the `uploads/teams/` and `uploads/players/` directories exist.

## Next Steps

1. Add your tournament teams
2. Add players to each team
3. Schedule your matches
4. Update match results as games complete
5. Share the public pages with fans!

---

**Enjoy your cricket tournament! 🏏**
