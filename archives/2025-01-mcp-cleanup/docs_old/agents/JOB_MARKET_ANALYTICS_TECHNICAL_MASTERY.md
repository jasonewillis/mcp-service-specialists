# Job Market Analytics Agent - Technical Mastery Knowledge Base

**Version**: 1.0  
**Date**: August 19, 2025  
**Purpose**: Technical expertise for Job Market Analytics MCP agent to research and provide market analysis guidance  
**Usage**: Knowledge base for researching job market trends and providing data-driven market analysis prompts  

---

## 🎯 **TECHNICAL MASTERY: Labor Market Data Analysis and Economic Research Implementation Expertise**

### **Labor Market Data Sources and Integration**

#### **Government Data APIs and Sources**
```yaml
Bureau of Labor Statistics (BLS):
  API Endpoints:
    Employment Statistics: "Current Employment Statistics (CES) for industry employment"
    Unemployment Data: "Local Area Unemployment Statistics (LAUS)"
    Job Openings: "Job Openings and Labor Turnover Survey (JOLTS)"
    Wage Data: "Occupational Employment and Wage Statistics (OEWS)"
    
    BLS API Implementation:
      import requests
      import pandas as pd
      from datetime import datetime, timedelta
      import json
      
      class BLSDataCollector:
          def __init__(self, api_key):
              self.api_key = api_key
              self.base_url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
              
          def get_employment_data(self, series_id, start_year, end_year):
              headers = {'Content-type': 'application/json'}
              data = json.dumps({
                  "seriesid": [series_id],
                  "startyear": str(start_year),
                  "endyear": str(end_year),
                  "registrationkey": self.api_key
              })
              
              response = requests.post(self.base_url, data=data, headers=headers)
              json_data = response.json()
              
              return self.parse_bls_response(json_data)
              
          def parse_bls_response(self, json_data):
              data_points = []
              for series in json_data['Results']['series']:
                  for item in series['data']:
                      data_points.append({
                          'year': item['year'],
                          'period': item['period'],
                          'value': float(item['value']) if item['value'] != 'null' else None,
                          'date': self.convert_period_to_date(item['year'], item['period'])
                      })
              
              return pd.DataFrame(data_points).sort_values('date')
          
          def get_federal_employment_trends(self):
              # Federal government employment series
              federal_series = "CES9091000001"  # Federal government employment
              current_year = datetime.now().year
              
              return self.get_employment_data(
                  federal_series, 
                  current_year - 5, 
                  current_year
              )

USAJOBS API Integration:
  Job Posting Analytics:
    Vacancy Announcements: "Current federal job openings data"
    Geographic Distribution: "Jobs by location and region"
    Salary Ranges: "Compensation data by position and grade"
    Application Deadlines: "Timeline analysis for federal hiring"
    
    USAJOBS Data Collection:
      class USAJOBSAnalyzer:
          def __init__(self, host, user_agent, authorization_key):
              self.base_url = "https://data.usajobs.gov/api/"
              self.headers = {
                  'Host': host,
                  'User-Agent': user_agent,
                  'Authorization-Key': authorization_key
              }
              
          def analyze_job_market_trends(self, days_back=30):
              # Get recent job postings
              date_from = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
              
              params = {
                  'DatePosted': date_from,
                  'Fields': 'min',  # Minimum fields for faster response
                  'Page': 1,
                  'ResultsPerPage': 500
              }
              
              all_jobs = []
              page = 1
              
              while True:
                  params['Page'] = page
                  response = requests.get(
                      f"{self.base_url}search",
                      headers=self.headers,
                      params=params
                  )
                  
                  if response.status_code != 200:
                      break
                      
                  data = response.json()
                  jobs = data.get('SearchResult', {}).get('SearchResultItems', [])
                  
                  if not jobs:
                      break
                      
                  all_jobs.extend(jobs)
                  page += 1
                  
                  if page > 10:  # Limit to prevent excessive API calls
                      break
              
              return self.analyze_job_patterns(all_jobs)
              
          def analyze_job_patterns(self, jobs_data):
              analysis = {
                  'total_positions': len(jobs_data),
                  'by_series': {},
                  'by_agency': {},
                  'by_location': {},
                  'by_grade_level': {},
                  'salary_trends': {},
                  'hiring_timeline': {}
              }
              
              for job in jobs_data:
                  job_details = job.get('MatchedObjectDescriptor', {})
                  
                  # Series analysis
                  series = job_details.get('JobCategory', [{}])[0].get('Code')
                  if series:
                      analysis['by_series'][series] = analysis['by_series'].get(series, 0) + 1
                  
                  # Agency analysis  
                  agency = job_details.get('OrganizationName')
                  if agency:
                      analysis['by_agency'][agency] = analysis['by_agency'].get(agency, 0) + 1
                  
                  # Location analysis
                  locations = job_details.get('PositionLocation', [])
                  for location in locations:
                      city_state = f"{location.get('CityName', 'Unknown')}, {location.get('StateName', 'Unknown')}"
                      analysis['by_location'][city_state] = analysis['by_location'].get(city_state, 0) + 1
                  
                  # Grade level analysis
                  grade_info = job_details.get('UserArea', {}).get('Details', {})
                  grade = grade_info.get('LowGrade', 'Unknown')
                  if grade != 'Unknown':
                      analysis['by_grade_level'][f"GS-{grade}"] = analysis['by_grade_level'].get(f"GS-{grade}", 0) + 1
              
              return analysis

O*NET Data Integration:
  Occupational Analysis:
    Skills Requirements: "Knowledge, Skills, Abilities for occupations"
    Work Activities: "Detailed work activity descriptions"
    Technology Skills: "Technology tools and software requirements"
    Career Pathways: "Related occupations and advancement paths"
    
    ONET Data Processing:
      class ONETAnalyzer:
          def __init__(self):
              self.onet_base = "https://services.onetcenter.org/ws/"
              
          def analyze_occupation_requirements(self, soc_code):
              occupation_data = {
                  'skills': self.get_occupation_skills(soc_code),
                  'abilities': self.get_occupation_abilities(soc_code),
                  'knowledge': self.get_occupation_knowledge(soc_code),
                  'technology': self.get_technology_skills(soc_code),
                  'work_activities': self.get_work_activities(soc_code)
              }
              
              return occupation_data
              
          def get_occupation_skills(self, soc_code):
              url = f"{self.onet_base}online/occupations/{soc_code}/summary/skills"
              response = requests.get(url)
              
              if response.status_code == 200:
                  data = response.json()
                  return [{
                      'skill': skill.get('element_name'),
                      'level': skill.get('score', {}).get('value'),
                      'importance': skill.get('score', {}).get('value')
                  } for skill in data.get('skill', [])]
              
              return []
          
          def identify_skill_gaps(self, current_skills, target_occupation):
              """Identify gaps between current skills and target occupation requirements"""
              target_requirements = self.analyze_occupation_requirements(target_occupation)
              
              skill_gaps = []
              for req_skill in target_requirements['skills']:
                  skill_name = req_skill['skill']
                  required_level = req_skill['level']
                  
                  current_level = current_skills.get(skill_name, 0)
                  
                  if current_level < required_level:
                      skill_gaps.append({
                          'skill': skill_name,
                          'current_level': current_level,
                          'required_level': required_level,
                          'gap_size': required_level - current_level
                      })
              
              return sorted(skill_gaps, key=lambda x: x['gap_size'], reverse=True)
```

#### **Alternative Data Sources and Web Scraping**
```yaml
Job Board Data Collection:
  LinkedIn Job Insights:
    Industry Trends: "Hiring activity by industry sector"
    Skills Demand: "Most requested skills in job postings"
    Salary Benchmarks: "Compensation ranges by role and location"
    
  Indeed Employment Trends:
    Job Search Volume: "Search activity for specific roles"
    Posting Frequency: "New job posting rates"
    Application Competition: "Average applications per posting"
    
    Web Scraping Framework:
      from selenium import webdriver
      from selenium.webdriver.common.by import By
      from bs4 import BeautifulSoup
      import time
      import random
      
      class JobBoardScraper:
          def __init__(self, headless=True):
              self.options = webdriver.ChromeOptions()
              if headless:
                  self.options.add_argument('--headless')
              self.driver = webdriver.Chrome(options=self.options)
              
          def scrape_indeed_trends(self, job_title, location, max_pages=5):
              job_data = []
              
              for page in range(max_pages):
                  url = f"https://www.indeed.com/jobs?q={job_title}&l={location}&start={page*10}"
                  self.driver.get(url)
                  time.sleep(random.uniform(2, 4))  # Random delay
                  
                  soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                  job_cards = soup.find_all('div', class_='job_seen_beacon')
                  
                  for card in job_cards:
                      job_info = self.extract_job_info(card)
                      if job_info:
                          job_data.append(job_info)
              
              return job_data
              
          def extract_job_info(self, job_card):
              try:
                  title = job_card.find('h2', class_='jobTitle').text.strip()
                  company = job_card.find('span', class_='companyName').text.strip()
                  location = job_card.find('div', class_='companyLocation').text.strip()
                  
                  # Extract salary if available
                  salary_element = job_card.find('span', class_='salary-snippet')
                  salary = salary_element.text.strip() if salary_element else None
                  
                  # Extract posting date
                  date_element = job_card.find('span', class_='date')
                  posted_date = date_element.text.strip() if date_element else None
                  
                  return {
                      'title': title,
                      'company': company,
                      'location': location,
                      'salary': salary,
                      'posted_date': posted_date,
                      'source': 'indeed'
                  }
              except Exception as e:
                  return None

Federal Contractor Data:
  SAM.gov Integration: "Federal contracting opportunities and awards"
  USASpending.gov: "Federal spending by agency and location"
  FPDS Data: "Federal procurement data system information"
  
  Contractor Market Analysis:
    def analyze_federal_contracting_trends(self):
        contracting_analysis = {
            'total_contract_value': 0,
            'by_agency': {},
            'by_location': {},
            'by_industry': {},
            'employment_impact': {},
            'growth_trends': {}
        }
        
        # Query USASpending API for recent contract awards
        usa_spending_api = "https://api.usaspending.gov/api/v2/"
        
        # Get contract awards data
        awards_endpoint = f"{usa_spending_api}search/spending_by_award/"
        
        payload = {
            "filters": {
                "award_type_codes": ["A", "B", "C", "D"],  # Contract types
                "time_period": [
                    {
                        "start_date": "2023-01-01",
                        "end_date": "2024-12-31"
                    }
                ]
            },
            "fields": ["Award ID", "Recipient Name", "Award Amount", "Awarding Agency"],
            "sort": "Award Amount",
            "order": "desc",
            "limit": 1000
        }
        
        response = requests.post(awards_endpoint, json=payload)
        
        if response.status_code == 200:
            awards_data = response.json()
            
            # Analyze contracting patterns
            for award in awards_data.get('results', []):
                agency = award.get('awarding_agency_name')
                amount = award.get('Award Amount', 0)
                
                contracting_analysis['total_contract_value'] += amount
                
                if agency:
                    contracting_analysis['by_agency'][agency] = \
                        contracting_analysis['by_agency'].get(agency, 0) + amount
        
        return contracting_analysis

Professional Association Data:
  Industry Reports: "Professional society employment surveys"
  Certification Trends: "Professional certification demand"
  Continuing Education: "Skills development requirements"
  
  Association Data Integration:
    professional_associations = {
        'technology': {
            'CompTIA': {
                'certifications': ['Security+', 'Network+', 'A+'],
                'salary_impact': 15,  # Percentage increase
                'demand_growth': 12   # Annual growth rate
            },
            'PMI': {
                'certifications': ['PMP', 'CAPM', 'PMI-ACP'],
                'salary_impact': 20,
                'demand_growth': 8
            }
        },
        'finance': {
            'CFA Institute': {
                'certifications': ['CFA', 'FRM'],
                'salary_impact': 25,
                'demand_growth': 6
            }
        }
    }
    
    def analyze_certification_trends(self, industry):
        if industry in professional_associations:
            cert_data = professional_associations[industry]
            
            analysis = {
                'recommended_certifications': [],
                'roi_analysis': {},
                'market_demand': {}
            }
            
            for org, details in cert_data.items():
                for cert in details['certifications']:
                    analysis['recommended_certifications'].append({
                        'certification': cert,
                        'organization': org,
                        'salary_impact': details['salary_impact'],
                        'demand_growth': details['demand_growth'],
                        'roi_score': details['salary_impact'] + details['demand_growth']
                    })
            
            # Sort by ROI score
            analysis['recommended_certifications'].sort(
                key=lambda x: x['roi_score'], reverse=True
            )
            
            return analysis
        
        return None
```

### **Statistical Analysis and Forecasting Methods**

#### **Time Series Analysis for Employment Trends**
```yaml
Employment Forecasting:
  Seasonal Adjustment:
    Purpose: "Remove seasonal variations to identify underlying trends"
    Methods: "X-13ARIMA-SEATS, seasonal decomposition"
    Application: "Federal hiring patterns, budget cycle impacts"
    
    Seasonal Analysis Implementation:
      import numpy as np
      import pandas as pd
      from statsmodels.tsa.seasonal import seasonal_decompose
      from statsmodels.tsa.arima.model import ARIMA
      from statsmodels.tsa.x13 import x13_arima_analysis
      
      class EmploymentForecaster:
          def __init__(self):
              self.models = {}
              
          def seasonal_adjustment(self, employment_data, frequency=12):
              """Remove seasonal components from employment time series"""
              
              # Convert to pandas time series
              ts = pd.Series(
                  employment_data['value'].values,
                  index=pd.to_datetime(employment_data['date'])
              )
              
              # Perform seasonal decomposition
              decomposition = seasonal_decompose(
                  ts, 
                  model='additive',
                  period=frequency
              )
              
              # Extract seasonally adjusted series
              seasonally_adjusted = ts - decomposition.seasonal
              
              return {
                  'original': ts,
                  'trend': decomposition.trend,
                  'seasonal': decomposition.seasonal,
                  'residual': decomposition.resid,
                  'seasonally_adjusted': seasonally_adjusted
              }
              
          def forecast_employment(self, historical_data, periods_ahead=12):
              """Generate employment forecasts using ARIMA modeling"""
              
              # Prepare time series data
              ts_data = self.prepare_time_series(historical_data)
              
              # Determine optimal ARIMA parameters
              best_aic = float('inf')
              best_order = None
              
              for p in range(3):
                  for d in range(2):
                      for q in range(3):
                          try:
                              model = ARIMA(ts_data, order=(p, d, q))
                              fitted_model = model.fit()
                              
                              if fitted_model.aic < best_aic:
                                  best_aic = fitted_model.aic
                                  best_order = (p, d, q)
                          except:
                              continue
              
              # Fit best model and generate forecasts
              if best_order:
                  final_model = ARIMA(ts_data, order=best_order)
                  fitted_final = final_model.fit()
                  
                  forecast = fitted_final.forecast(steps=periods_ahead)
                  confidence_intervals = fitted_final.get_forecast(periods_ahead).conf_int()
                  
                  return {
                      'forecast': forecast,
                      'confidence_intervals': confidence_intervals,
                      'model_order': best_order,
                      'aic': best_aic,
                      'fitted_model': fitted_final
                  }
              
              return None

Trend Analysis:
  Growth Rate Calculations:
    Compound Annual Growth Rate: "CAGR for long-term employment trends"
    Month-over-Month Changes: "Short-term employment volatility"
    Year-over-Year Comparisons: "Annual employment cycle analysis"
    
    Growth Analysis:
      def calculate_employment_growth_rates(self, employment_data):
          growth_analysis = {
              'cagr': {},
              'mom_growth': [],
              'yoy_growth': [],
              'volatility_metrics': {}
          }
          
          # Sort data by date
          data_sorted = employment_data.sort_values('date')
          
          # Calculate CAGR for different periods
          for years in [1, 3, 5, 10]:
              if len(data_sorted) >= years * 12:  # Assuming monthly data
                  start_value = data_sorted.iloc[0]['value']
                  end_value = data_sorted.iloc[years * 12 - 1]['value']
                  
                  cagr = ((end_value / start_value) ** (1/years)) - 1
                  growth_analysis['cagr'][f'{years}_year'] = cagr * 100
          
          # Calculate month-over-month growth
          for i in range(1, len(data_sorted)):
              prev_value = data_sorted.iloc[i-1]['value']
              curr_value = data_sorted.iloc[i]['value']
              
              if prev_value != 0:
                  mom_growth = ((curr_value - prev_value) / prev_value) * 100
                  growth_analysis['mom_growth'].append({
                      'date': data_sorted.iloc[i]['date'],
                      'growth_rate': mom_growth
                  })
          
          # Calculate year-over-year growth
          for i in range(12, len(data_sorted)):  # Start from 13th month
              prev_year_value = data_sorted.iloc[i-12]['value']
              curr_value = data_sorted.iloc[i]['value']
              
              if prev_year_value != 0:
                  yoy_growth = ((curr_value - prev_year_value) / prev_year_value) * 100
                  growth_analysis['yoy_growth'].append({
                      'date': data_sorted.iloc[i]['date'],
                      'growth_rate': yoy_growth
                  })
          
          # Calculate volatility metrics
          if growth_analysis['mom_growth']:
              mom_rates = [item['growth_rate'] for item in growth_analysis['mom_growth']]
              growth_analysis['volatility_metrics']['mom_std'] = np.std(mom_rates)
              growth_analysis['volatility_metrics']['mom_cv'] = np.std(mom_rates) / np.mean(mom_rates) if np.mean(mom_rates) != 0 else 0
          
          return growth_analysis

Correlation Analysis:
  Economic Indicators: "Relationship between employment and economic metrics"
  Leading Indicators: "Predictive variables for employment changes"
  Regional Correlations: "Geographic employment interdependencies"
  
  Correlation Framework:
    def analyze_employment_correlations(self, employment_data, economic_indicators):
        correlation_analysis = {
            'correlation_matrix': {},
            'leading_indicators': {},
            'lagged_correlations': {},
            'significance_tests': {}
        }
        
        # Merge employment data with economic indicators
        combined_data = self.merge_time_series(employment_data, economic_indicators)
        
        # Calculate correlation matrix
        correlation_matrix = combined_data.corr()
        correlation_analysis['correlation_matrix'] = correlation_matrix.to_dict()
        
        # Identify leading indicators through lagged correlations
        employment_column = 'employment'
        for indicator in economic_indicators.columns:
            if indicator != employment_column:
                lagged_corrs = []
                
                for lag in range(1, 13):  # Test lags up to 12 months
                    lagged_indicator = combined_data[indicator].shift(lag)
                    correlation = combined_data[employment_column].corr(lagged_indicator)
                    
                    if not np.isnan(correlation):
                        lagged_corrs.append({
                            'lag': lag,
                            'correlation': correlation
                        })
                
                # Find optimal lag (highest absolute correlation)
                if lagged_corrs:
                    best_lag = max(lagged_corrs, key=lambda x: abs(x['correlation']))
                    correlation_analysis['leading_indicators'][indicator] = best_lag
        
        return correlation_analysis
```

#### **Geographic and Demographic Analysis**
```yaml
Regional Employment Analysis:
  Metropolitan Statistical Areas:
    MSA Classifications: "Major metropolitan employment markets"
    Commuting Patterns: "Inter-regional labor mobility"
    Cost of Living Adjustments: "Real wage comparisons across regions"
    
    Geographic Analysis Framework:
      import geopandas as gpd
      from shapely.geometry import Point
      import folium
      
      class GeographicAnalyzer:
          def __init__(self):
              self.msa_boundaries = None
              self.state_boundaries = None
              
          def load_geographic_data(self):
              # Load MSA and state boundary data
              self.msa_boundaries = gpd.read_file('msa_boundaries.shp')
              self.state_boundaries = gpd.read_file('state_boundaries.shp')
              
          def analyze_regional_employment(self, job_data):
              regional_analysis = {
                  'by_msa': {},
                  'by_state': {},
                  'employment_density': {},
                  'growth_hotspots': []
              }
              
              # Convert job locations to geographic points
              job_points = []
              for job in job_data:
                  if job.get('latitude') and job.get('longitude'):
                      point = Point(job['longitude'], job['latitude'])
                      job_points.append({
                          'geometry': point,
                          'job_data': job
                      })
              
              job_gdf = gpd.GeoDataFrame(job_points)
              
              # Spatial join with MSA boundaries
              if self.msa_boundaries is not None:
                  jobs_with_msa = gpd.sjoin(job_gdf, self.msa_boundaries, how='left')
                  
                  # Count jobs by MSA
                  msa_counts = jobs_with_msa.groupby('MSA_NAME').size()
                  regional_analysis['by_msa'] = msa_counts.to_dict()
              
              return regional_analysis
              
          def calculate_employment_density(self, job_counts, geographic_areas):
              """Calculate jobs per square mile for different regions"""
              density_analysis = {}
              
              for region, job_count in job_counts.items():
                  if region in geographic_areas:
                      area_sq_miles = geographic_areas[region]['area']
                      density = job_count / area_sq_miles
                      
                      density_analysis[region] = {
                          'jobs_per_sq_mile': density,
                          'total_jobs': job_count,
                          'area_sq_miles': area_sq_miles
                      }
              
              return density_analysis
              
          def identify_growth_hotspots(self, historical_job_data, threshold_growth=0.1):
              """Identify regions with above-threshold employment growth"""
              hotspots = []
              
              for region in historical_job_data.keys():
                  region_data = historical_job_data[region]
                  
                  if len(region_data) >= 24:  # Need at least 2 years of data
                      recent_avg = np.mean(region_data[-12:])  # Last 12 months
                      previous_avg = np.mean(region_data[-24:-12])  # Previous 12 months
                      
                      if previous_avg > 0:
                          growth_rate = (recent_avg - previous_avg) / previous_avg
                          
                          if growth_rate >= threshold_growth:
                              hotspots.append({
                                  'region': region,
                                  'growth_rate': growth_rate,
                                  'recent_employment': recent_avg,
                                  'classification': 'high_growth'
                              })
              
              return sorted(hotspots, key=lambda x: x['growth_rate'], reverse=True)

Demographic Workforce Analysis:
  Age Distribution: "Workforce demographics by generation"
  Education Levels: "Educational attainment requirements and trends"
  Skills Gaps: "Mismatch between available and required skills"
  
  Demographic Analysis:
    def analyze_workforce_demographics(self, workforce_data):
        demographic_analysis = {
            'age_distribution': {},
            'education_levels': {},
            'experience_requirements': {},
            'skills_analysis': {},
            'diversity_metrics': {}
        }
        
        # Age distribution analysis
        age_bins = [(18, 24), (25, 34), (35, 44), (45, 54), (55, 64), (65, 99)]
        for min_age, max_age in age_bins:
            age_group = f"{min_age}-{max_age}"
            count = len([w for w in workforce_data if min_age <= w.get('age', 0) <= max_age])
            demographic_analysis['age_distribution'][age_group] = count
        
        # Education level analysis
        education_levels = ['High School', 'Associates', 'Bachelors', 'Masters', 'PhD']
        for edu_level in education_levels:
            count = len([w for w in workforce_data if w.get('education') == edu_level])
            demographic_analysis['education_levels'][edu_level] = count
        
        # Experience requirements analysis
        experience_bins = [(0, 2), (3, 5), (6, 10), (11, 15), (16, 99)]
        for min_exp, max_exp in experience_bins:
            exp_group = f"{min_exp}-{max_exp} years"
            count = len([w for w in workforce_data 
                        if min_exp <= w.get('years_experience', 0) <= max_exp])
            demographic_analysis['experience_requirements'][exp_group] = count
        
        return demographic_analysis

Federal Workforce Composition:
  GS Grade Distribution: "Federal employment by grade level"
  Occupational Series: "Distribution across job series"
  Agency Composition: "Employment by federal agency"
  Remote Work Trends: "Telework and remote position analysis"
  
  Federal Analysis:
    def analyze_federal_workforce_composition(self, federal_employment_data):
        federal_analysis = {
            'gs_grade_distribution': {},
            'occupational_series': {},
            'agency_composition': {},
            'remote_work_trends': {},
            'retirement_projections': {}
        }
        
        # GS Grade analysis
        for employee in federal_employment_data:
            grade = employee.get('grade', 'Unknown')
            if grade.startswith('GS-'):
                grade_num = grade.replace('GS-', '')
                federal_analysis['gs_grade_distribution'][grade_num] = \
                    federal_analysis['gs_grade_distribution'].get(grade_num, 0) + 1
        
        # Occupational series analysis
        for employee in federal_employment_data:
            series = employee.get('occupational_series', 'Unknown')
            federal_analysis['occupational_series'][series] = \
                federal_analysis['occupational_series'].get(series, 0) + 1
        
        # Agency composition
        for employee in federal_employment_data:
            agency = employee.get('agency', 'Unknown')
            federal_analysis['agency_composition'][agency] = \
                federal_analysis['agency_composition'].get(agency, 0) + 1
        
        # Remote work trends
        remote_count = len([e for e in federal_employment_data 
                           if e.get('remote_eligible', False)])
        total_count = len(federal_employment_data)
        
        federal_analysis['remote_work_trends'] = {
            'remote_eligible_positions': remote_count,
            'total_positions': total_count,
            'remote_percentage': (remote_count / total_count) * 100 if total_count > 0 else 0
        }
        
        return federal_analysis
```

### **Market Intelligence and Competitive Analysis**

#### **Salary and Compensation Analysis**
```yaml
Compensation Benchmarking:
  Federal Pay Scales:
    GS Pay Tables: "General Schedule salary ranges by grade and step"
    Locality Adjustments: "Geographic cost-of-living adjustments"
    Special Pay Systems: "SES, SL, ST special salary systems"
    
    Federal Compensation Analysis:
      class FederalCompensationAnalyzer:
          def __init__(self):
              self.current_year = datetime.now().year
              self.gs_pay_table = self.load_gs_pay_table()
              self.locality_adjustments = self.load_locality_adjustments()
              
          def load_gs_pay_table(self):
              # GS pay table for current year (simplified structure)
              return {
                  '5': {'1': 30113, '10': 39149},
                  '7': {'1': 37301, '10': 48488},
                  '9': {'1': 46083, '10': 59316},
                  '11': {'1': 55756, '10': 72487},
                  '12': {'1': 66829, '10': 86881},
                  '13': {'1': 79468, '10': 103309},
                  '14': {'1': 93907, '10': 122077},
                  '15': {'1': 110460, '10': 143598}
              }
              
          def calculate_federal_salary(self, grade, step, locality):
              """Calculate total federal salary including locality adjustment"""
              base_salary = self.gs_pay_table.get(str(grade), {}).get(str(step))
              
              if base_salary:
                  locality_multiplier = self.locality_adjustments.get(locality, 1.0)
                  total_salary = base_salary * locality_multiplier
                  
                  return {
                      'base_salary': base_salary,
                      'locality_adjustment': locality_multiplier,
                      'total_salary': total_salary,
                      'grade': grade,
                      'step': step,
                      'locality': locality
                  }
              
              return None
              
          def compare_federal_vs_private(self, job_title, location, experience_level):
              """Compare federal and private sector compensation"""
              comparison = {
                  'federal': {},
                  'private': {},
                  'differential': {},
                  'total_compensation': {}
              }
              
              # Estimate federal compensation
              estimated_grade = self.estimate_gs_grade(job_title, experience_level)
              federal_comp = self.calculate_federal_salary(estimated_grade, 5, location)
              
              if federal_comp:
                  # Add federal benefits value (approximately 30% of salary)
                  federal_benefits_value = federal_comp['total_salary'] * 0.30
                  
                  comparison['federal'] = {
                      'base_salary': federal_comp['total_salary'],
                      'benefits_value': federal_benefits_value,
                      'total_compensation': federal_comp['total_salary'] + federal_benefits_value
                  }
              
              # Estimate private sector compensation (would integrate with salary APIs)
              private_salary_estimate = self.estimate_private_salary(job_title, location, experience_level)
              private_benefits_value = private_salary_estimate * 0.25  # Typically lower than federal
              
              comparison['private'] = {
                  'base_salary': private_salary_estimate,
                  'benefits_value': private_benefits_value,
                  'total_compensation': private_salary_estimate + private_benefits_value
              }
              
              # Calculate differential
              comparison['differential'] = {
                  'salary_difference': comparison['federal']['base_salary'] - comparison['private']['base_salary'],
                  'total_comp_difference': comparison['federal']['total_compensation'] - comparison['private']['total_compensation']
              }
              
              return comparison

Benefits Analysis:
  Federal Benefits Package:
    Health Insurance: "FEHB premium costs and coverage options"
    Retirement Systems: "FERS vs CSRS retirement calculations"
    Thrift Savings Plan: "TSP contribution matching and investment options"
    Leave Accrual: "Annual and sick leave accumulation rates"
    
  Private Sector Comparison:
    401k Plans: "Employer matching and vesting schedules"
    Healthcare Costs: "Premium and deductible comparisons"
    Stock Options: "Equity compensation potential"
    Flexible Benefits: "PTO, flexible schedules, remote work options"
    
    Benefits Valuation:
      def calculate_benefits_value(self, salary, sector='federal'):
          benefits_breakdown = {}
          
          if sector == 'federal':
              # Federal benefits calculation
              benefits_breakdown = {
                  'health_insurance': {
                      'employer_contribution': salary * 0.10,  # ~10% of salary
                      'description': 'FEHB employer contribution'
                  },
                  'retirement': {
                      'fers_basic': salary * 0.008,  # 0.8% employer contribution
                      'tsp_match': min(salary * 0.05, salary * 0.05),  # Up to 5% match
                      'social_security': salary * 0.062,  # Employer portion
                      'description': 'FERS retirement system'
                  },
                  'leave': {
                      'annual_leave_value': (salary / 2080) * 26,  # 26 days/year average
                      'sick_leave_value': (salary / 2080) * 13,  # 13 days/year
                      'description': 'Paid time off value'
                  },
                  'life_insurance': {
                      'fegli_basic': salary * 0.002,  # Basic FEGLI cost
                      'description': 'Federal life insurance'
                  }
              }
              
          elif sector == 'private':
              # Private sector benefits (more variable)
              benefits_breakdown = {
                  'health_insurance': {
                      'employer_contribution': salary * 0.08,  # ~8% average
                      'description': 'Private health insurance contribution'
                  },
                  'retirement': {
                      '401k_match': min(salary * 0.04, salary * 0.06),  # 4-6% typical
                      'social_security': salary * 0.062,
                      'description': '401k and social security'
                  },
                  'leave': {
                      'pto_value': (salary / 2080) * 20,  # 20 days average
                      'description': 'Paid time off'
                  },
                  'bonus_potential': {
                      'annual_bonus': salary * 0.10,  # 10% potential bonus
                      'description': 'Performance bonus potential'
                  }
              }
          
          # Calculate total benefits value
          total_benefits = sum(
              sum(benefit.values()) if isinstance(benefit, dict) 
              else benefit
              for benefit in benefits_breakdown.values()
              if isinstance(benefit, (dict, int, float))
          )
          
          return {
              'breakdown': benefits_breakdown,
              'total_value': total_benefits,
              'percentage_of_salary': (total_benefits / salary) * 100
          }

Market Position Analysis:
  Competitive Intelligence:
    Employer Branding: "Federal government as employer attractiveness"
    Talent Acquisition: "Recruitment effectiveness and time-to-hire"
    Retention Rates: "Employee turnover analysis"
    
  Skills Premium Analysis:
    High-Demand Skills: "Skills commanding salary premiums"
    Certification Value: "ROI of professional certifications"
    Experience Curves: "Salary progression by years of experience"
    
    Skills Premium Calculator:
      def calculate_skills_premium(self, base_salary, skills_list):
          """Calculate salary premium for specific skills"""
          
          # Skills premium database (percentage increases)
          skills_premiums = {
              'cybersecurity': 15,
              'data_science': 20,
              'machine_learning': 25,
              'cloud_computing': 18,
              'project_management': 12,
              'agile_methodology': 8,
              'python_programming': 15,
              'sql_database': 10,
              'security_clearance': 22,
              'government_experience': 8
          }
          
          premium_analysis = {
              'base_salary': base_salary,
              'skill_premiums': {},
              'total_premium': 0,
              'adjusted_salary': base_salary
          }
          
          total_premium_percentage = 0
          
          for skill in skills_list:
              skill_lower = skill.lower().replace(' ', '_')
              
              if skill_lower in skills_premiums:
                  premium_percentage = skills_premiums[skill_lower]
                  premium_amount = base_salary * (premium_percentage / 100)
                  
                  premium_analysis['skill_premiums'][skill] = {
                      'percentage': premium_percentage,
                      'amount': premium_amount
                  }
                  
                  total_premium_percentage += premium_percentage
          
          # Apply diminishing returns for multiple skills
          if total_premium_percentage > 50:
              total_premium_percentage = 50 + (total_premium_percentage - 50) * 0.5
          
          premium_analysis['total_premium'] = base_salary * (total_premium_percentage / 100)
          premium_analysis['adjusted_salary'] = base_salary + premium_analysis['total_premium']
          
          return premium_analysis
```

---

## 🎯 **Agent Implementation Guidance**

### **How This Technical Mastery Enhances Agent Performance**

#### **Market Research and Data Analysis**
- **Data Integration**: Advanced techniques for combining multiple data sources (BLS, USAJOBS, O*NET, private markets)
- **Statistical Analysis**: Sophisticated forecasting, trend analysis, and correlation methods
- **Geographic Intelligence**: Spatial analysis capabilities for regional employment patterns
- **Compensation Analysis**: Comprehensive salary and benefits benchmarking frameworks

#### **Problem-Solving Approach**
- **Market Intelligence**: Expert guidance on employment trends, skills demand, and competitive positioning
- **Predictive Analytics**: Advanced forecasting methods for employment and salary trends
- **Comparative Analysis**: Sophisticated frameworks for federal vs. private sector comparisons
- **Strategic Insights**: Data-driven recommendations for career planning and market positioning

### **Agent Usage Instructions**

#### **When to Apply This Technical Knowledge**
```python
# Example usage in agent decision-making
if market_analysis_request == "employment_trends":
    collect_bls_employment_data()
    apply_seasonal_adjustment()
    generate_employment_forecasts()
    
if compensation_analysis_needed == "salary_benchmarking":
    analyze_federal_pay_scales()
    compare_private_sector_rates()
    calculate_total_compensation_packages()
    
if skills_analysis == "demand_forecasting":
    integrate_onet_skills_data()
    analyze_job_posting_requirements()
    calculate_skills_premium_values()
```

#### **Research Output Enhancement**
All Job Market Analytics agent research should include:
- **Data-driven employment analysis** with statistical forecasting and trend identification
- **Comprehensive compensation benchmarking** with federal and private sector comparisons
- **Geographic market intelligence** with regional employment patterns and growth hotspots
- **Skills demand analysis** with premium calculations and certification ROI assessment
- **Competitive positioning insights** with market trends and strategic recommendations

---

*This technical mastery knowledge base transforms the Job Market Analytics Agent from basic market research to comprehensive labor market analysis expertise, enabling sophisticated data integration, statistical forecasting, and strategic market intelligence for federal career planning and employment decision-making.*

**© 2025 Fed Job Advisor - Job Market Analytics Agent Technical Mastery Enhancement**