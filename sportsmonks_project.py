import os
import requests
from datetime import datetime
from supabase import create_client, Client

# Configurações
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
API_KEY = os.environ.get('API_KEY', '4vYK7knP9N1sy4eASn0lluLzxuXDiIQWafJgtdjG64dmTjHqEdgHM962xESQ')
LOG_FILE = 'script.log'
LEAGUE_ID = 1479  # CONCACAF League
BASE_URL = 'https://api.sportmonks.com/v3/football'

# Inicializando cliente supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def log_message(message: str) -> None:
    with open(LOG_FILE, 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'{timestamp} - {message}\n')
    print(message)

def get_fixtures() -> list:
    url = f"{BASE_URL}/fixtures?api_token={API_KEY}&leagues={LEAGUE_ID}&include=participants"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json().get('data', [])

def insert_matches(matches: list) -> int:
    if not matches:
        return 0

    data_to_insert = []
    for m in matches:
        participants = m.get('participants', [])
        if len(participants) < 2:
            log_message(f"Warning: Missing participants for match {m.get('id')}. Skipping...")
            continue

        match_date = m.get('starting_at')
        home_team = participants[0].get('name')
        away_team = participants[1].get('name')
        data_to_insert.append(
            {
                "match_date": match_date,
                "home_team": home_team,
                "away_team": away_team,
                "competition": "CONCACAF League",
                "season": "2025"
            }
        )

    if not data_to_insert:
        return 0

    # Insert into supabase
    result = supabase.table('matches').insert(data_to_insert).execute()
    log_message(f"Inserted {len(data_to_insert)} matches into supabase.")
    return len(data_to_insert)

if __name__ == '__main__':
    try:
        fixtures = get_fixtures()
        num_inserted = insert_matches(fixtures)
        log_message(f'Inserted {num_inserted} matches successfully.')
    except Exception as e:
        log_message(f'Error: {e}')
