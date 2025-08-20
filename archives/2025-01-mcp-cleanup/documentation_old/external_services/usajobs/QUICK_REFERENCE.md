# USAJobs API Quick Reference

## Copy-Paste Template

```python
import requests
import time

# CRITICAL: Never forget these
BASE_URL = 'https://data.usajobs.gov/api/search'
PARAMS = {
    'Fields': 'Full',  # MANDATORY - prevents 93% data loss
    'ResultsPerPage': 500,
    'Keyword': 'your search terms'
}

HEADERS = {
    'Authorization-Key': 'YOUR_API_KEY',
    'User-Agent': 'your.email@example.com'
}

# Make request with rate limiting
response = requests.get(BASE_URL, params=PARAMS, headers=HEADERS)
time.sleep(1.2)  # Rate limit: 50 req/min
```
