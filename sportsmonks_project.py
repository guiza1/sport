import os
import requests
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime

# Configurações
DATABASE_URL = 'postgres://postgres:S2amd:pgdhuahua@db.wlpbhvpsoymgacckfyn.supabase.co:5432/postgres'
API_KEY = '4vYK7knP9N1sy4eASn0lluLzxuXDiIQWafJgtdjG64dmTjHqEdgHM962xESQ'
LOG_FILE = 'script.log'
LEAGUE_ID = 1479  # CONCACAF League
BASE_URL = 'https://api.sportmonks.com/v3/football'

def log_message(message):
    with open(LOG_FILE, 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'{timestamp} - {message}\n')

def get_fixtures():
    # Incluindo os participantes
    url = f"{BASE_URL}/fixtures?api_token={API_KEY}&leagues={LEAGUE_ID}&include=participants"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json().get('data', [])

def insert_matches(matches):
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
        data_to_insert.append((match_date, home_team, away_team, 'CONCACAF League', '2025'))

    if not data_to_insert:
        return 0

    sql = (
        'INSERT INTO matches (match_date, home_team, away_team, competition, season) '
        'VALUES %s '
        'ON CONFLICT DO NOTHING;'
    )
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            execute_values(cur, sql, data_to_insert)
        conn.commit()

    return len(data_to_insert)

if __name__ == '__main__':
    try:
        fixtures = get_fixtures()
        num_inserted = insert_matches(fixtures)
        log_message(f'Inserted {num_inserted} matches successfully.')
    except Exception as e:
        log_message(f'Error: {e}')

