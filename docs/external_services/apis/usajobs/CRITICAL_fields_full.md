# ⚠️ CRITICAL: USAJobs API Parameters

## 🚨 NEVER FORGET THESE PARAMETERS 🚨

### THE #1 RULE: Always Include Fields=Full

```python
# CORRECT - Gets all data
url = 'https://data.usajobs.gov/api/search?Fields=Full&Keyword=data'

# WRONG - Loses 93% of data
url = 'https://data.usajobs.gov/api/search?Keyword=data'  # NO NO NO!
```

### Fields
- **Value**: `Full`
- **Importance**: CRITICAL
- **Why**: Without this, you lose 93% of data including job_summary, qualification_summary
- **⚠️ WARNING**: Missing Fields=Full causes catastrophic data loss
- **Example**: `https://data.usajobs.gov/api/search?Fields=Full&Keyword=data%20scientist`

### ResultsPerPage
- **Value**: `500`
- **Importance**: HIGH
- **Why**: Maximum results per request for efficient collection
- **Example**: `&ResultsPerPage=500`

### Authorization-Key
- **Value**: `YOUR_API_KEY`
- **Importance**: CRITICAL
- **Why**: Required header for authentication
- **Example**: `headers={'Authorization-Key': 'your-key-here'}`

### User-Agent
- **Value**: `YOUR_EMAIL`
- **Importance**: REQUIRED
- **Why**: Your email for API tracking
- **Example**: `headers={'User-Agent': 'your.email@example.com'}`

### Rate-Limit
- **Value**: `50 requests/minute`
- **Importance**: CRITICAL
- **Why**: Exceeding this will block your API key
- **Example**: `time.sleep(1.2) between requests`

