import os
import time
import requests
from datetime import datetime
from supabase import create_client, Client

# Configurações
SUPABASE_URL = "db.wlpbhvpsoymgacckfyny.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndscGJodnBzb3ltZ2FjY2tmeW55Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA1NDAyMzMsImV4cCI6MjA2NjExNjIzM30.-VnugrGaT_rehXPTy7P2TTQkl_Sh2Cqdc7OMaozkhU0"
API_KEY = "4vYK7knP9N1sy4eASn0lluLzxuXDiIQWafJgtdjG64dmTjHqEdgHM962xESQ"
LOG_FILE = "script.log"
LEAGUE_ID = 1479
BASE_URL = "https://api.sportmonks.com/v3/football"
INTERVAL_SECONDS = 21600  # 6 horas

# Cliente supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def log_message(message):
    with open(LOG_FILE, 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'{timestamp} - {message}\n')

def get_fixtures():
    url = f"{BASE_URL}/fixtures?api_token={API_KEY}&leagues={LEAGUE_ID}&include=participants"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json().get('data', [])

def insert_matches(matches):
    data_to_insert = []
    for m in matches:
        participants = m.get('participants', [])
        if len(participants) < 2:
            log_message(f"Warning: Missing participants for match {m.get('id')}. Skipping...")
            continue
        data_to_insert.append(
            {
                "match_date": m.get('starting_at'),
                "home_team": participants[0].get('name'),
                "away_team": participants[1].get('name'),
                "competition": "CONCACAF League",
                "season": "2025"
            }
        )

    if not data_to_insert:
        return 0

    # Inserindo os dados
    result = supabase.table("matches").insert(data_to_insert).execute()
    log_message(f"{len(data_to_insert)} matches inserted successfully with status {result.status_code}")
    return len(data_to_insert)

if __name__ == '__main__':
    while True:
        try:
            fixtures = get_fixtures()
            num_inserted = insert_matches(fixtures)
        except Exception as e:
            log_message(f"Error: {e}")
        log_message(f"Sleeping for {INTERVAL_SECONDS} seconds...")
        time.sleep(INTERVAL_SECONDS)
