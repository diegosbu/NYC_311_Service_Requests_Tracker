# NYC 311 Data Pull - Pulls 311 service requests data from the last 2 days and inserts into a database

import os
from dotenv import load_dotenv

import pandas as pd
from datetime import datetime, timezone, timedelta
from sodapy import Socrata

load_dotenv()

app_token = os.getenv('NYC_APP_TOKEN')

def main():
    # Set Socrata client parameters
    client = Socrata(
        'data.cityofnewyork.us',
        app_token,
        timeout=60
    )

    # Set current UTC date minus 2 days
    date_requested = (datetime.now(timezone.utc) + timedelta(days=-2)).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%dT%H:%M:%S')

    # Get 311 service requests from last 2 days
    with client:
        results = client.get(
            'erm2-nwe9', 
            where = f"created_date >= '{date_requested}'",
            limit = 5,
            order = 'created_date DESC'
        )
    
    # Convert results to dataframe
    df = pd.DataFrame(results)

    
main()

