#!/usr/bin/env python3
"""
Live Agent Dashboard for Virtual Development Team
"""

import streamlit as st
import requests
import json
import time
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuration
API_URL = "http://localhost:8003"

st.set_page_config(
    page_title="Virtual Dev Team Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .agent-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def check_api_status():
    """Check if API is running"""
    try:
        response = requests.get(f"{API_URL}/", timeout=2)
        return response.json() if response.status_code == 200 else None
    except:
        return None

def test_agent(role, task):
    """Test an agent with a task"""
    try:
        response = requests.post(
            f"{API_URL}/test/{role}",
            params={"task": task},
            timeout=30
        )
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        return {"error": str(e)}

def compare_models(task):
    """Compare models on same task"""
    try:
        response = requests.post(
            f"{API_URL}/compare",
            params={"task": task},
            timeout=60
        )
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        return {"error": str(e)}

# Main Dashboard
st.markdown('<h1 class="main-header">🚀 Virtual Development Team Dashboard</h1>', unsafe_allow_html=True)

# Check API Status
api_status = check_api_status()

if api_status:
    # Status indicators
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("System Status", "🟢 Online")
    with col2:
        st.metric("Available Models", len(api_status.get("models", [])))
    with col3:
        st.metric("API Endpoint", "localhost:8003")
    with col4:
        st.metric("Last Check", datetime.now().strftime("%H:%M:%S"))
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🤖 Agent Testing", "🔬 Model Comparison", "📊 Performance", "⚙️ Configuration"])
    
    with tab1:
        st.header("Test Individual Agents")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            agent_role = st.selectbox(
                "Select Agent Role",
                ["backend", "frontend", "data", "devops", "security", "pm"],
                format_func=lambda x: {
                    "backend": "🔧 Backend Engineer",
                    "frontend": "🎨 Frontend Developer",
                    "data": "📊 Data Scientist",
                    "devops": "🚀 DevOps Engineer",
                    "security": "🔒 Security Analyst",
                    "pm": "📋 Project Manager"
                }.get(x, x)
            )
            
            task_presets = {
                "backend": [
                    "Create a REST API endpoint for user authentication",
                    "Optimize this database query for performance",
                    "Write unit tests for a payment service"
                ],
                "frontend": [
                    "Create a responsive navigation menu component",
                    "Implement infinite scroll with React",
                    "Add dark mode to a website"
                ],
                "data": [
                    "Analyze customer churn patterns",
                    "Build a recommendation system",
                    "Create a sales forecast model"
                ],
                "devops": [
                    "Create a CI/CD pipeline for Python app",
                    "Write a Dockerfile for Node.js application",
                    "Set up monitoring with Prometheus"
                ],
                "security": [
                    "Perform security audit on REST API",
                    "Identify vulnerabilities in this code",
                    "Create a security policy document"
                ],
                "pm": [
                    "Break down epic into user stories",
                    "Create sprint planning for 2 weeks",
                    "Write project status update"
                ]
            }
            
            preset = st.selectbox(
                "Task Preset",
                ["Custom"] + task_presets.get(agent_role, [])
            )
            
            if preset == "Custom":
                task = st.text_area("Enter Task", height=100)
            else:
                task = preset
                st.info(f"Task: {task}")
        
        with col2:
            if st.button("🚀 Execute Task", type="primary", use_container_width=True):
                if task:
                    with st.spinner(f"Agent {agent_role} is working..."):
                        start_time = time.time()
                        result = test_agent(agent_role, task)
                        elapsed = time.time() - start_time
                    
                    if result and "error" not in result:
                        st.success(f"✅ Task completed in {elapsed:.2f}s")
                        
                        # Display response
                        st.subheader("Agent Response")
                        response_container = st.container()
                        with response_container:
                            st.markdown(result.get("response", "No response"))
                        
                        # Metrics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Model Used", result.get("model", "Unknown"))
                        with col2:
                            st.metric("Tokens Generated", result.get("eval_count", 0))
                        with col3:
                            st.metric("Response Time", f"{elapsed:.2f}s")
                    else:
                        st.error(f"Error: {result.get('error', 'Unknown error')}")
    
    with tab2:
        st.header("Model Comparison")
        
        comparison_task = st.text_input(
            "Enter task for comparison",
            value="Write a Python function to find the longest common subsequence"
        )
        
        if st.button("🔬 Compare Models", type="primary"):
            with st.spinner("Comparing models..."):
                comparison = compare_models(comparison_task)
            
            if comparison and "error" not in comparison:
                # Remove winner from results for display
                winner = comparison.pop("winner", None)
                
                # Display winner
                if winner:
                    st.success(f"🏆 Winner: **{winner}** (fastest response)")
                
                # Create comparison table
                comparison_data = []
                for model, results in comparison.items():
                    if isinstance(results, dict) and "error" not in results:
                        comparison_data.append({
                            "Model": model,
                            "Response Time": f"{results.get('time', 0):.2f}s",
                            "Tokens": results.get('tokens', 0),
                            "Response Preview": results.get('response', '')[:100] + "..."
                        })
                
                if comparison_data:
                    df = pd.DataFrame(comparison_data)
                    st.dataframe(df, use_container_width=True)
                    
                    # Visualization
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Time comparison
                        times = {m: r.get('time', 0) for m, r in comparison.items() 
                                if isinstance(r, dict) and 'time' in r}
                        if times:
                            fig = px.bar(
                                x=list(times.keys()),
                                y=list(times.values()),
                                title="Response Time Comparison",
                                labels={'x': 'Model', 'y': 'Time (seconds)'}
                            )
                            st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        # Token comparison
                        tokens = {m: r.get('tokens', 0) for m, r in comparison.items() 
                                 if isinstance(r, dict) and 'tokens' in r}
                        if tokens:
                            fig = px.bar(
                                x=list(tokens.keys()),
                                y=list(tokens.values()),
                                title="Token Count Comparison",
                                labels={'x': 'Model', 'y': 'Tokens Generated'}
                            )
                            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.header("Performance Metrics")
        
        # Placeholder for performance tracking
        st.info("Performance tracking will show historical data once multiple tests are run")
        
        # Sample performance data
        performance_data = {
            "Timestamp": pd.date_range(start="2025-01-14 13:00", periods=10, freq="5min"),
            "Response Time": [2.3, 1.8, 3.1, 2.5, 1.9, 2.7, 2.1, 1.7, 2.4, 2.0],
            "Tokens": [450, 380, 520, 410, 390, 480, 420, 370, 460, 400]
        }
        
        df_perf = pd.DataFrame(performance_data)
        
        # Response time trend
        fig1 = px.line(df_perf, x="Timestamp", y="Response Time", 
                      title="Response Time Trend", markers=True)
        st.plotly_chart(fig1, use_container_width=True)
        
        # Token usage trend
        fig2 = px.area(df_perf, x="Timestamp", y="Tokens", 
                       title="Token Usage Over Time")
        st.plotly_chart(fig2, use_container_width=True)
    
    with tab4:
        st.header("System Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Available Models")
            for model in api_status.get("models", []):
                st.write(f"• {model}")
        
        with col2:
            st.subheader("Agent Roles")
            roles = {
                "backend": "Backend Engineer",
                "frontend": "Frontend Developer",
                "data": "Data Scientist",
                "devops": "DevOps Engineer",
                "security": "Security Analyst",
                "pm": "Project Manager"
            }
            for key, value in roles.items():
                st.write(f"• **{key}**: {value}")
        
        st.subheader("API Information")
        st.json(api_status)

else:
    st.error("❌ API is not running!")
    st.warning("Please start the controller first:")
    st.code("""
# In terminal:
cd /Users/jasonewillis/Developer/jwRepos/JLWAI/Agents
source venv/bin/activate
python start_controller_simple.py
    """)

# Sidebar
with st.sidebar:
    st.header("🎮 Quick Actions")
    
    if st.button("🔄 Refresh Status"):
        st.rerun()
    
    st.header("📚 Documentation")
    st.markdown("""
    **Virtual Dev Team**
    - 6 specialized agents
    - Powered by llama3.1:70b
    - Local execution (no API costs)
    
    **Agent Roles:**
    - 🔧 Backend Engineer
    - 🎨 Frontend Developer
    - 📊 Data Scientist
    - 🚀 DevOps Engineer
    - 🔒 Security Analyst
    - 📋 Project Manager
    """)
    
    st.header("🔗 Links")
    st.markdown("""
    - [API Docs](http://localhost:8002/docs)
    - [GitHub Repo](https://github.com/JLWAI/Agents)
    """)

# Auto-refresh
if st.checkbox("Auto-refresh (10s)", value=False):
    time.sleep(10)
    st.rerun()