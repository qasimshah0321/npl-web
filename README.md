# NPL Cricket Tournament Management System

A comprehensive web application for managing cricket tournaments with team management, player statistics, match scheduling, and tournament bracket visualization.

## Features

### Public Features
- **Landing Page**: Tournament overview with latest match results and statistics
- **Match Schedule**: Complete match schedule with results highlighted in green for winners
- **Teams Page**: View all participating teams with logos and details
- **Players Page**: Browse all players with statistics and search functionality
- **Tournament Bracket**: Visual representation of tournament progression

### Admin Features
- **Team Management**: Add, edit, delete teams and upload team logos
- **Player Management**: Manage players with photos and detailed statistics
- **Match Management**: Schedule matches and update results
- **Tournament Settings**: Configure tournament details and settings
- **Statistics Dashboard**: Real-time overview of teams, players, and matches

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Authentication**: Flask-Login with session management
- **Styling**: Cricket-themed responsive design

## Installation

### 1. Clone or Navigate to the Project

```bash
cd "E:\Personal-projects\CludeCode\NPL Web"
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
python backend/app.py
```

The application will be available at `http://localhost:5000`

## Default Credentials

**Admin Login:**
- Username: `admin`
- Password: `admin123`

**Important**: Change these credentials in production!

## Project Structure

```
NPL Web/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── models.py              # Database models
│   ├── database.py            # Database utilities
│   ├── auth.py                # Authentication routes
│   ├── config.py              # Configuration
│   └── api/
│       ├── teams.py           # Team endpoints
│       ├── players.py         # Player endpoints
│       ├── matches.py         # Match endpoints
│       └── tournament.py      # Tournament endpoints
├── frontend/
│   ├── index.html             # Landing page
│   ├── login.html             # Login page
│   ├── teams.html             # Teams page
│   ├── players.html           # Players page
│   ├── schedule.html          # Schedule page
│   ├── bracket.html           # Bracket page
│   ├── admin.html             # Admin dashboard
│   ├── css/
│   │   ├── style.css          # Main styles
│   │   └── admin.css          # Admin styles
│   └── js/
│       ├── main.js            # Shared utilities
│       └── admin.js           # Admin functionality
├── uploads/
│   ├── teams/                 # Team logos
│   └── players/               # Player photos
├── database/
│   └── cricket.db             # SQLite database
└── requirements.txt           # Python dependencies
```

## Database Schema

The application uses 6 main tables:

1. **users**: User authentication and roles
2. **teams**: Team information and logos
3. **players**: Player details and team associations
4. **player_statistics**: Detailed player statistics
5. **matches**: Match scheduling and results
6. **tournament_settings**: Tournament configuration

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/check` - Check auth status

### Teams
- `GET /api/teams` - Get all teams
- `GET /api/teams/<id>` - Get team details
- `POST /api/teams` - Create team (admin)
- `PUT /api/teams/<id>` - Update team (admin)
- `DELETE /api/teams/<id>` - Delete team (admin)
- `POST /api/teams/<id>/logo` - Upload logo (admin)

### Players
- `GET /api/players` - Get all players
- `GET /api/players/<id>` - Get player details
- `POST /api/players` - Create player (admin)
- `PUT /api/players/<id>` - Update player (admin)
- `DELETE /api/players/<id>` - Delete player (admin)
- `PUT /api/players/<id>/stats` - Update stats (admin)

### Matches
- `GET /api/matches` - Get all matches
- `GET /api/matches/<id>` - Get match details
- `POST /api/matches` - Create match (admin)
- `PUT /api/matches/<id>` - Update match (admin)
- `PUT /api/matches/<id>/result` - Update result (admin)
- `DELETE /api/matches/<id>` - Delete match (admin)

### Tournament
- `GET /api/tournament/settings` - Get settings
- `PUT /api/tournament/settings` - Update settings (admin)
- `GET /api/tournament/bracket` - Get bracket structure

## Usage Guide

### For Administrators

1. **Login**: Navigate to `/login.html` and use admin credentials
2. **Add Teams**: Go to Admin Dashboard > Teams tab > Add New Team
3. **Add Players**: Teams tab > Players tab > Add New Player
4. **Schedule Matches**: Matches tab > Add New Match
5. **Update Results**: Matches tab > Result button for each match
6. **Configure Tournament**: Tournament tab > Update settings

### For Viewers

1. **View Schedule**: Check match dates, times, and results
2. **Explore Teams**: Browse team information and rosters
3. **View Players**: Search and filter players by stats
4. **Follow Bracket**: Track tournament progression

## Features Highlight

### Cricket-Themed Design
- Green and red color scheme (cricket field + ball)
- Cricket ball and bat icons
- Stadium-inspired backgrounds
- Card-based layouts
- Responsive mobile-first design

### Match Schedule Table
- Date, Day, Match, Venue, Round columns
- **Winning teams highlighted in GREEN**
- Filter by rounds (Round 1, Round 2, Semi-Final, Final)
- Real-time status updates

### Player Statistics
- Runs scored, wickets taken
- Balls faced, balls bowled
- Fours, sixes, catches, stumpings
- Searchable and sortable

## Development Notes

### Adding Sample Data

You can add sample teams and players through the admin dashboard, or directly insert into the database.

### Customization

- Colors: Edit CSS variables in `/frontend/css/style.css`
- Tournament rounds: Modify round options in match forms
- Player roles: Update role options in player forms

## Troubleshooting

### Database Issues
- The database is automatically created on first run
- Location: `database/cricket.db`
- To reset: Delete the database file and restart the application

### Upload Issues
- Ensure `uploads/teams/` and `uploads/players/` directories exist
- Check file permissions
- Maximum upload size: 5MB

### Port Already in Use
- Change port in `backend/app.py` (default: 5000)
- Or stop other applications using port 5000

## Future Enhancements

- Live score updates during matches
- Player performance graphs
- Tournament history and archives
- Email notifications
- Mobile app integration
- Advanced statistics and analytics

## License

This project is created for cricket tournament management.

## Deployment

### Deploy to Production

This application is ready to deploy! See detailed guides:

- **[QUICKSTART.md](QUICKSTART.md)** - Quick deployment guide
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Comprehensive deployment options

**Recommended hosting:**
- **Render.com** (Free tier, easiest setup)
- Railway.app
- Heroku
- Netlify (frontend) + Render (backend)

Quick deploy to Render.com:
1. Push code to GitHub
2. Connect Render.com to your repository
3. Deploy automatically with `render.yaml`

## Support

For issues or questions, please check:
1. This README file
2. [DEPLOYMENT.md](DEPLOYMENT.md) for hosting help
3. Application logs in the console
4. Database schema in `backend/database.py`

---

**Enjoy managing your cricket tournament! 🏏**
