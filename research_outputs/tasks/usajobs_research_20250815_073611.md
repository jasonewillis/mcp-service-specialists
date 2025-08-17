# USAJobs API Research Report

**Generated**: 2025-08-15T07:36:11.063747
**Task**: Implement job search for data scientist positions in DC
**Type**: search

## Critical Requirements
- ALWAYS include Fields=Full parameter in every API call
- Include Authorization-Key header with valid API key
- Include User-Agent header with email address
- Respect rate limit of 50 requests per minute
- Use ResultsPerPage=500 for efficient collection
- Handle pagination with Page parameter
- Check PositionEndDate for expired jobs
- Parse location data from PositionLocation array

## Implementation Plan
Implementation plan for search operation

### Steps
1. Setup request headers with authentication
2. Build search parameters with Fields=Full
3. Execute search request
4. Parse response and extract jobs
5. Handle pagination if needed

## API Endpoints
- **Primary job search**: `https://data.usajobs.gov/api/search`
  - Required: Fields=Full

## Parameters
### Required
- `Fields=Full`

## Best Practices
- Use existing collect_federal_jobs.py as reference
- Test with small dataset first
- Log all API responses for debugging
- Handle network errors with exponential backoff
