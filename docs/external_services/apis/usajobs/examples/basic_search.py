#!/usr/bin/env python3
"""
USAJobs Basic Search Example
CRITICAL: Always use Fields=Full
"""

import requests

# Configuration
API_KEY = "YOUR_API_KEY"
USER_AGENT = "your-email@example.com"

# Headers (all required)
headers = {
    'Authorization-Key': API_KEY,
    'User-Agent': USER_AGENT,
    'Host': 'data.usajobs.gov'
}

# Search parameters
params = {
    'Fields': 'Full',  # CRITICAL - Without this, you lose 93% of data!
    'ResultsPerPage': 250,
    'Page': 1,
    'DatePosted': 7,  # Last 7 days
    'LocationName': 'Washington, DC'
}

# Make request
response = requests.get(
    'https://data.usajobs.gov/api/Search/jobs',
    headers=headers,
    params=params
)

if response.status_code == 200:
    data = response.json()
    jobs = data['SearchResult']['SearchResultItems']
    
    # Verify Fields=Full worked
    if jobs and jobs[0].get('MatchedObjectDescriptor', {}).get('UserArea', {}).get('Details'):
        print(f"✅ Successfully retrieved {len(jobs)} jobs with full details")
    else:
        print("❌ WARNING: Missing job details! Check Fields=Full parameter")
else:
    print(f"Error {response.status_code}: {response.text}")
