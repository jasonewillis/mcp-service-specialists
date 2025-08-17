# USAJobs API Reference

## Base URL
```
https://data.usajobs.gov/api/
```

## Authentication
```python
headers = {
    'Authorization-Key': 'YOUR_API_KEY',
    'User-Agent': 'your.email@example.com'
}
```

## Endpoints

### SEARCH
- **URL**: `https://data.usajobs.gov/api/search`
- **Method**: GET
- **Description**: Primary job search endpoint
- **REQUIRED**: Fields=Full
- **Common Parameters**: Keyword, LocationName, JobCategoryCode, Organization, SalaryBucket, GradeBucket, PostedDate, ResultsPerPage, Page

### CODELIST
- **URL**: `https://data.usajobs.gov/api/codelist`
- **Method**: GET
- **Description**: Get reference data (agencies, series, etc.)

