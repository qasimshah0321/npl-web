// Admin Dashboard JavaScript

let teams = [];
let players = [];
let matches = [];
let selectedPlayers = new Set();

// Check admin authentication
async function checkAdminAuth() {
    const auth = await checkAuth();
    if (!auth.authenticated || auth.user.role !== 'admin') {
        window.location.href = '/login.html';
    }
}

// Tab Switching
function switchTab(tabName) {
    document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));

    event.target.classList.add('active');
    document.getElementById(tabName + 'Tab').classList.add('active');
}

// Modal Functions
function showModal(modalId) {
    document.getElementById(modalId).classList.add('active');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

// Load Statistics
async function loadStats() {
    try {
        const [teamsRes, playersRes, matchesRes] = await Promise.all([
            fetch('/api/teams'),
            fetch('/api/players'),
            fetch('/api/matches')
        ]);

        teams = await teamsRes.json();
        players = await playersRes.json();
        matches = await matchesRes.json();

        document.getElementById('statTeams').textContent = teams.length;
        document.getElementById('statPlayers').textContent = players.length;
        document.getElementById('statMatches').textContent = matches.length;
    } catch (error) {
        console.error('Failed to load stats:', error);
    }
}

// ===== TEAMS MANAGEMENT =====

async function loadTeams() {
    try {
        const response = await fetch('/api/teams');
        teams = await response.json();

        const tbody = document.getElementById('teamsTableBody');
        if (teams.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="empty-state">No teams found</td></tr>';
            return;
        }

        tbody.innerHTML = teams.map(team => `
            <tr>
                <td><strong>${team.name}</strong></td>
                <td>${team.coach_name || 'N/A'}</td>
                <td>${team.home_ground || 'N/A'}</td>
                <td>${team.player_count || 0}</td>
                <td class="action-buttons">
                    <button class="btn btn-secondary btn-small" onclick="editTeam(${team.id})">Edit</button>
                    <button class="btn btn-danger btn-small" onclick="deleteTeam(${team.id})">Delete</button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Failed to load teams:', error);
    }
}

function showAddTeamModal() {
    document.getElementById('teamModalTitle').textContent = 'Add Team';
    document.getElementById('teamForm').reset();
    document.getElementById('teamId').value = '';
    showModal('teamModal');
}

async function editTeam(id) {
    const team = teams.find(t => t.id === id);
    if (!team) return;

    document.getElementById('teamModalTitle').textContent = 'Edit Team';
    document.getElementById('teamId').value = team.id;
    document.getElementById('teamName').value = team.name;
    document.getElementById('coachName').value = team.coach_name || '';
    document.getElementById('homeGround').value = team.home_ground || '';
    showModal('teamModal');
}

async function deleteTeam(id) {
    if (!confirm('Are you sure you want to delete this team?')) return;

    try {
        const response = await fetch(`/api/teams/${id}`, {
            method: 'DELETE',
            credentials: 'include'
        });

        if (response.ok) {
            alert('Team deleted successfully');
            loadTeams();
            loadStats();
        } else {
            const data = await response.json();
            alert('Error: ' + (data.error || 'Failed to delete team'));
        }
    } catch (error) {
        alert('Error deleting team');
    }
}

// Team Form Submit
document.getElementById('teamForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const teamId = document.getElementById('teamId').value;
    const teamData = {
        name: document.getElementById('teamName').value,
        coach_name: document.getElementById('coachName').value,
        home_ground: document.getElementById('homeGround').value
    };

    try {
        const url = teamId ? `/api/teams/${teamId}` : '/api/teams';
        const method = teamId ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify(teamData)
        });

        if (response.ok) {
            const data = await response.json();

            // Handle logo upload if file selected
            const logoFile = document.getElementById('teamLogo').files[0];
            if (logoFile && data.team_id) {
                const formData = new FormData();
                formData.append('logo', logoFile);

                await fetch(`/api/teams/${data.team_id || teamId}/logo`, {
                    method: 'POST',
                    credentials: 'include',
                    body: formData
                });
            }

            alert(teamId ? 'Team updated successfully' : 'Team created successfully');
            closeModal('teamModal');
            loadTeams();
            loadStats();
        } else {
            const data = await response.json();
            alert('Error: ' + (data.error || 'Failed to save team'));
        }
    } catch (error) {
        alert('Error saving team');
    }
});

// ===== PLAYERS MANAGEMENT =====

async function loadPlayers() {
    try {
        const response = await fetch('/api/players');
        players = await response.json();

        const tbody = document.getElementById('playersTableBody');
        if (players.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="empty-state">No players found</td></tr>';
            return;
        }

        tbody.innerHTML = players.map(player => `
            <tr>
                <td>
                    <input type="checkbox"
                           class="player-checkbox"
                           data-player-id="${player.id}"
                           ${selectedPlayers.has(player.id) ? 'checked' : ''}
                           onchange="togglePlayerSelection(${player.id})"
                           style="width: 18px; height: 18px; cursor: pointer;">
                </td>
                <td><strong>${player.name}</strong></td>
                <td>${player.team_name}</td>
                <td>${player.role}</td>
                <td>${player.jersey_number || 'N/A'}</td>
                <td>${player.runs_scored || 0} runs, ${player.wickets_taken || 0} wickets</td>
                <td class="action-buttons">
                    <button class="btn btn-secondary btn-small" onclick="editPlayer(${player.id})">Edit</button>
                    <button class="btn btn-danger btn-small" onclick="deletePlayer(${player.id})">Delete</button>
                </td>
            </tr>
        `).join('');

        updatePlayerSelectionUI();
    } catch (error) {
        console.error('Failed to load players:', error);
    }
}

async function showAddPlayerModal() {
    await populateTeamSelects();
    document.getElementById('playerModalTitle').textContent = 'Add Player';
    document.getElementById('playerForm').reset();
    document.getElementById('playerId').value = '';
    showModal('playerModal');
}

async function editPlayer(id) {
    const player = players.find(p => p.id === id);
    if (!player) return;

    await populateTeamSelects();
    document.getElementById('playerModalTitle').textContent = 'Edit Player';
    document.getElementById('playerId').value = player.id;
    document.getElementById('playerName').value = player.name;
    document.getElementById('playerTeam').value = player.team_id;
    document.getElementById('playerRole').value = player.role;
    document.getElementById('jerseyNumber').value = player.jersey_number || '';
    document.getElementById('battingStyle').value = player.batting_style || '';
    document.getElementById('bowlingStyle').value = player.bowling_style || '';
    showModal('playerModal');
}

async function deletePlayer(id) {
    if (!confirm('Are you sure you want to delete this player?')) return;

    try {
        const response = await fetch(`/api/players/${id}`, {
            method: 'DELETE',
            credentials: 'include'
        });

        if (response.ok) {
            alert('Player deleted successfully');
            loadPlayers();
            loadStats();
        } else {
            const data = await response.json();
            alert('Error: ' + (data.error || 'Failed to delete player'));
        }
    } catch (error) {
        alert('Error deleting player');
    }
}

// Player Form Submit
document.getElementById('playerForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const playerId = document.getElementById('playerId').value;
    const playerData = {
        name: document.getElementById('playerName').value,
        team_id: parseInt(document.getElementById('playerTeam').value),
        role: document.getElementById('playerRole').value,
        jersey_number: parseInt(document.getElementById('jerseyNumber').value) || null,
        batting_style: document.getElementById('battingStyle').value,
        bowling_style: document.getElementById('bowlingStyle').value
    };

    try {
        const url = playerId ? `/api/players/${playerId}` : '/api/players';
        const method = playerId ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify(playerData)
        });

        if (response.ok) {
            alert(playerId ? 'Player updated successfully' : 'Player created successfully');
            closeModal('playerModal');
            loadPlayers();
            loadStats();
        } else {
            const data = await response.json();
            alert('Error: ' + (data.error || 'Failed to save player'));
        }
    } catch (error) {
        alert('Error saving player');
    }
});

// ===== MATCHES MANAGEMENT =====

async function loadMatches() {
    try {
        const response = await fetch('/api/matches');
        matches = await response.json();

        const tbody = document.getElementById('matchesTableBody');
        if (matches.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="empty-state">No matches found</td></tr>';
            return;
        }

        tbody.innerHTML = matches.map(match => `
            <tr>
                <td>${formatDate(match.match_date)}</td>
                <td><strong>${match.team_a_name} vs ${match.team_b_name}</strong></td>
                <td>${match.venue || 'TBD'}</td>
                <td>${match.round}</td>
                <td>${match.status}</td>
                <td class="action-buttons">
                    <button class="btn btn-secondary btn-small" onclick="updateResult(${match.id})">Result</button>
                    <button class="btn btn-secondary btn-small" onclick="editMatch(${match.id})">Edit</button>
                    <button class="btn btn-danger btn-small" onclick="deleteMatch(${match.id})">Delete</button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Failed to load matches:', error);
    }
}

async function showAddMatchModal() {
    await populateTeamSelects();
    document.getElementById('matchModalTitle').textContent = 'Add Match';
    document.getElementById('matchForm').reset();
    document.getElementById('matchId').value = '';
    showModal('matchModal');
}

async function editMatch(id) {
    const match = matches.find(m => m.id === id);
    if (!match) return;

    await populateTeamSelects();
    document.getElementById('matchModalTitle').textContent = 'Edit Match';
    document.getElementById('matchId').value = match.id;
    document.getElementById('matchDate').value = match.match_date;
    document.getElementById('matchTime').value = match.match_time || '';
    document.getElementById('teamA').value = match.team_a_id;
    document.getElementById('teamB').value = match.team_b_id;
    document.getElementById('venue').value = match.venue || '';
    document.getElementById('round').value = match.round;
    showModal('matchModal');
}

async function deleteMatch(id) {
    if (!confirm('Are you sure you want to delete this match?')) return;

    try {
        const response = await fetch(`/api/matches/${id}`, {
            method: 'DELETE',
            credentials: 'include'
        });

        if (response.ok) {
            alert('Match deleted successfully');
            loadMatches();
            loadStats();
        } else {
            const data = await response.json();
            alert('Error: ' + (data.error || 'Failed to delete match'));
        }
    } catch (error) {
        alert('Error deleting match');
    }
}

async function updateResult(id) {
    const match = matches.find(m => m.id === id);
    if (!match) return;

    document.getElementById('resultMatchId').value = match.id;

    // Populate winner select
    const winnerSelect = document.getElementById('winnerId');
    winnerSelect.innerHTML = `
        <option value="${match.team_a_id}">${match.team_a_name}</option>
        <option value="${match.team_b_id}">${match.team_b_name}</option>
    `;

    if (match.winner_id) {
        winnerSelect.value = match.winner_id;
        document.getElementById('teamAScore').value = match.team_a_score || '';
        document.getElementById('teamBScore').value = match.team_b_score || '';
        document.getElementById('resultSummary').value = match.result_summary || '';
    }

    showModal('resultModal');
}

// Match Form Submit
document.getElementById('matchForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const matchId = document.getElementById('matchId').value;
    const date = new Date(document.getElementById('matchDate').value);

    const matchData = {
        match_date: document.getElementById('matchDate').value,
        match_day: date.toLocaleDateString('en-US', { weekday: 'long' }),
        team_a_id: parseInt(document.getElementById('teamA').value),
        team_b_id: parseInt(document.getElementById('teamB').value),
        venue: document.getElementById('venue').value,
        match_time: document.getElementById('matchTime').value,
        round: document.getElementById('round').value
    };

    try {
        const url = matchId ? `/api/matches/${matchId}` : '/api/matches';
        const method = matchId ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify(matchData)
        });

        if (response.ok) {
            alert(matchId ? 'Match updated successfully' : 'Match created successfully');
            closeModal('matchModal');
            loadMatches();
            loadStats();
        } else {
            const data = await response.json();
            alert('Error: ' + (data.error || 'Failed to save match'));
        }
    } catch (error) {
        alert('Error saving match');
    }
});

// Result Form Submit
document.getElementById('resultForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const matchId = document.getElementById('resultMatchId').value;
    const resultData = {
        winner_id: parseInt(document.getElementById('winnerId').value),
        team_a_score: document.getElementById('teamAScore').value,
        team_b_score: document.getElementById('teamBScore').value,
        result_summary: document.getElementById('resultSummary').value
    };

    try {
        const response = await fetch(`/api/matches/${matchId}/result`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify(resultData)
        });

        if (response.ok) {
            alert('Result updated successfully');
            closeModal('resultModal');
            loadMatches();
        } else {
            const data = await response.json();
            alert('Error: ' + (data.error || 'Failed to update result'));
        }
    } catch (error) {
        alert('Error updating result');
    }
});

// ===== TOURNAMENT SETTINGS =====

async function loadTournamentSettings() {
    try {
        const response = await fetch('/api/tournament/settings');
        const settings = await response.json();

        document.getElementById('tournamentName').value = settings.tournament_name;
        document.getElementById('totalTeams').value = settings.total_teams;
        document.getElementById('startDate').value = settings.start_date || '';
        document.getElementById('endDate').value = settings.end_date || '';
    } catch (error) {
        console.error('Failed to load tournament settings:', error);
    }
}

document.getElementById('tournamentForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const settingsData = {
        tournament_name: document.getElementById('tournamentName').value,
        total_teams: parseInt(document.getElementById('totalTeams').value),
        start_date: document.getElementById('startDate').value,
        end_date: document.getElementById('endDate').value
    };

    try {
        const response = await fetch('/api/tournament/settings', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify(settingsData)
        });

        if (response.ok) {
            alert('Tournament settings updated successfully');
        } else {
            const data = await response.json();
            alert('Error: ' + (data.error || 'Failed to update settings'));
        }
    } catch (error) {
        alert('Error updating settings');
    }
});

// ===== UTILITY FUNCTIONS =====

async function populateTeamSelects() {
    if (teams.length === 0) {
        const response = await fetch('/api/teams');
        teams = await response.json();
    }

    const selects = [
        document.getElementById('playerTeam'),
        document.getElementById('teamA'),
        document.getElementById('teamB')
    ];

    selects.forEach(select => {
        if (select) {
            select.innerHTML = '<option value="">Select Team</option>' +
                teams.map(team => `<option value="${team.id}">${team.name}</option>`).join('');
        }
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', async () => {
    await checkAdminAuth();
    loadStats();
    loadTeams();
    loadPlayers();
    loadMatches();
    loadTournamentSettings();
});

// ===== BULK DELETE PLAYERS =====

function togglePlayerSelection(playerId) {
    if (selectedPlayers.has(playerId)) {
        selectedPlayers.delete(playerId);
    } else {
        selectedPlayers.add(playerId);
    }
    updatePlayerSelectionUI();
}

function toggleSelectAllPlayers() {
    const selectAllCheckbox = document.getElementById('selectAllPlayers');
    if (selectAllCheckbox.checked) {
        // Select all players
        players.forEach(player => selectedPlayers.add(player.id));
    } else {
        // Deselect all
        selectedPlayers.clear();
    }
    loadPlayers(); // Refresh to update checkboxes
}

function updatePlayerSelectionUI() {
    const selectedCount = selectedPlayers.size;
    document.getElementById('selectedPlayersCount').textContent = selectedCount;
    document.getElementById('bulkDeletePlayersBtn').style.display = selectedCount > 0 ? 'inline-block' : 'none';

    // Update select all checkbox
    const selectAllCheckbox = document.getElementById('selectAllPlayers');
    if (selectAllCheckbox) {
        selectAllCheckbox.checked = selectedCount > 0 && selectedCount === players.length;
        selectAllCheckbox.indeterminate = selectedCount > 0 && selectedCount < players.length;
    }
}

async function bulkDeletePlayers() {
    if (selectedPlayers.size === 0) {
        alert('No players selected');
        return;
    }

    const confirmMsg = `Are you sure you want to delete ${selectedPlayers.size} player(s)? This action cannot be undone.`;
    if (!confirm(confirmMsg)) {
        return;
    }

    try {
        const response = await fetch('/api/players/bulk-delete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify({
                player_ids: Array.from(selectedPlayers)
            })
        });

        const data = await response.json();

        if (response.ok) {
            alert(data.message);
            selectedPlayers.clear();
            loadPlayers();
            loadStats();
        } else {
            alert('Error: ' + (data.error || 'Failed to delete players'));
        }
    } catch (error) {
        console.error('Failed to delete players:', error);
        alert('Failed to delete players. Please try again.');
    }
}
