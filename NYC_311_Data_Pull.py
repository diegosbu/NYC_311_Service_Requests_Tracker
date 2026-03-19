# NYC 311 Data Pull - Pulls 311 service requests data from the last 2 days and inserts into a database

import os
from dotenv import load_dotenv

import pandas as pd
from datetime import datetime, timezone, timedelta
import requests

load_dotenv()

app_token = os.getenv('NYC_APP_TOKEN')

def main():
    # Set current UTC date minus 2 days
    date_requested = (datetime.now(timezone.utc) + timedelta(days=-2)).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%dT%H:%M:%S')
    
    url = 'https://data.cityofnewyork.us/api/v3/views/erm2-nwe9/query.json'

    data = requests.post( 
                        url,
                        headers = { 'X-App-Token': f'{app_token}' },
                        json = { 'query': f"SELECT unique_key, status, created_date, agency, complaint_type, descriptor, incident_address, incident_zip, \
                                                    city, resolution_action_updated_date, resolution_description, closed_date  \
                                            WHERE created_date >= '{date_requested}' \
                                                OR resolution_action_updated_date >= '{date_requested}' \
                                            ORDER BY created_date DESC"
                                }
                    ).json()
    
    df = pd.DataFrame(data).filter(regex='^[^:].*')
        
main()

