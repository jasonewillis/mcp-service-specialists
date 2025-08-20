"""
A/B Test Dashboard for Agent Model Comparison
Interactive visualization of model performance across agent roles
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from pathlib import Path
from datetime import datetime
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Agent Model A/B Testing Dashboard",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

class ABTestDashboard:
    """Dashboard for visualizing A/B test results"""
    
    def __init__(self):
        self.results_dir = Path("test_results")
        self.results_dir.mkdir(exist_ok=True)
        
    def load_test_results(self):
        """Load all test results from CSV files"""
        csv_files = list(self.results_dir.glob("*.csv"))
        
        if not csv_files:
            return pd.DataFrame()
        
        dfs = []
        for file in csv_files:
            try:
                df = pd.read_csv(file)
                dfs.append(df)
            except Exception as e:
                st.error(f"Error loading {file}: {e}")
        
        if dfs:
            return pd.concat(dfs, ignore_index=True)
        return pd.DataFrame()
    
    def load_comparison_results(self):
        """Load comparison JSON files"""
        json_files = list(self.results_dir.glob("comparison_*.json"))
        comparisons = []
        
        for file in json_files:
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                    comparisons.append(data)
            except Exception as e:
                st.error(f"Error loading {file}: {e}")
        
        return comparisons
    
    def render_dashboard(self):
        """Main dashboard rendering"""
        
        # Title and description
        st.title("🧪 Agent Model A/B Testing Dashboard")
        st.markdown("""
        Compare performance of different LLM models across various agent roles.
        This dashboard helps identify the best model for each specific task.
        """)
        
        # Load data
        df = self.load_test_results()
        comparisons = self.load_comparison_results()
        
        if df.empty:
            st.warning("No test results found. Run some A/B tests first!")
            self.render_test_runner()
            return
        
        # Sidebar filters
        st.sidebar.header("🔍 Filters")
        
        selected_models = st.sidebar.multiselect(
            "Select Models",
            options=df['model'].unique() if 'model' in df else [],
            default=df['model'].unique() if 'model' in df else []
        )
        
        selected_roles = st.sidebar.multiselect(
            "Select Agent Roles",
            options=df['agent_role'].unique() if 'agent_role' in df else [],
            default=df['agent_role'].unique() if 'agent_role' in df else []
        )
        
        # Filter dataframe
        if selected_models and selected_roles:
            filtered_df = df[
                (df['model'].isin(selected_models)) & 
                (df['agent_role'].isin(selected_roles))
            ]
        else:
            filtered_df = df
        
        # Main metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_tests = len(filtered_df)
            st.metric("Total Tests", f"{total_tests:,}")
        
        with col2:
            if 'passed' in filtered_df:
                pass_rate = filtered_df['passed'].mean() * 100
                st.metric("Overall Pass Rate", f"{pass_rate:.1f}%")
        
        with col3:
            if 'score' in filtered_df:
                avg_score = filtered_df['score'].mean()
                st.metric("Average Score", f"{avg_score:.2f}")
        
        with col4:
            if 'execution_time' in filtered_df:
                avg_time = filtered_df['execution_time'].mean()
                st.metric("Avg Execution Time", f"{avg_time:.2f}s")
        
        # Tabs for different views
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Overview",
            "🏆 Model Comparison",
            "👥 Agent Performance",
            "📈 Detailed Analysis",
            "🔬 Test Runner"
        ])
        
        with tab1:
            self.render_overview(filtered_df)
        
        with tab2:
            self.render_model_comparison(filtered_df)
        
        with tab3:
            self.render_agent_performance(filtered_df)
        
        with tab4:
            self.render_detailed_analysis(filtered_df, comparisons)
        
        with tab5:
            self.render_test_runner()
    
    def render_overview(self, df):
        """Render overview charts"""
        st.header("Performance Overview")
        
        if df.empty:
            st.info("No data to display")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Pass rate by model
            if 'model' in df and 'passed' in df:
                pass_by_model = df.groupby('model')['passed'].mean() * 100
                fig = px.bar(
                    x=pass_by_model.index,
                    y=pass_by_model.values,
                    title="Pass Rate by Model",
                    labels={'x': 'Model', 'y': 'Pass Rate (%)'},
                    color=pass_by_model.values,
                    color_continuous_scale='RdYlGn'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Average score by agent role
            if 'agent_role' in df and 'score' in df:
                score_by_role = df.groupby('agent_role')['score'].mean()
                fig = px.bar(
                    x=score_by_role.index,
                    y=score_by_role.values,
                    title="Average Score by Agent Role",
                    labels={'x': 'Agent Role', 'y': 'Average Score'},
                    color=score_by_role.values,
                    color_continuous_scale='Viridis'
                )
                fig.update_xaxis(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
        
        # Heatmap of model performance by role
        if all(col in df for col in ['model', 'agent_role', 'score']):
            st.subheader("Model Performance Heatmap")
            pivot_table = df.pivot_table(
                values='score',
                index='agent_role',
                columns='model',
                aggfunc='mean'
            )
            
            fig = px.imshow(
                pivot_table,
                labels=dict(x="Model", y="Agent Role", color="Score"),
                x=pivot_table.columns,
                y=pivot_table.index,
                color_continuous_scale='RdYlGn',
                aspect="auto"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def render_model_comparison(self, df):
        """Render model comparison view"""
        st.header("Model Comparison")
        
        if df.empty or 'model' not in df:
            st.info("No model data to display")
            return
        
        models = df['model'].unique()
        
        # Create comparison metrics
        comparison_data = []
        for model in models:
            model_df = df[df['model'] == model]
            comparison_data.append({
                'Model': model,
                'Tests': len(model_df),
                'Pass Rate': model_df['passed'].mean() * 100 if 'passed' in model_df else 0,
                'Avg Score': model_df['score'].mean() if 'score' in model_df else 0,
                'Avg Time': model_df['execution_time'].mean() if 'execution_time' in model_df else 0,
                'Avg Tokens': model_df['tokens_used'].mean() if 'tokens_used' in model_df else 0
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        
        # Display comparison table
        st.subheader("Model Metrics Comparison")
        st.dataframe(
            comparison_df.style.highlight_max(axis=0, subset=['Pass Rate', 'Avg Score'])
                              .highlight_min(axis=0, subset=['Avg Time', 'Avg Tokens']),
            use_container_width=True
        )
        
        # Radar chart for model comparison
        if len(models) > 1:
            st.subheader("Model Capabilities Radar")
            
            categories = ['Pass Rate', 'Avg Score', 'Speed', 'Efficiency']
            
            fig = go.Figure()
            
            for model in models[:5]:  # Limit to 5 models for clarity
                model_df = df[df['model'] == model]
                
                # Normalize metrics to 0-100 scale
                pass_rate = model_df['passed'].mean() * 100 if 'passed' in model_df else 0
                avg_score = model_df['score'].mean() * 100 if 'score' in model_df else 0
                
                # Speed: inverse of time (faster is better)
                avg_time = model_df['execution_time'].mean() if 'execution_time' in model_df else 1
                speed = min(100, (1 / avg_time) * 100) if avg_time > 0 else 0
                
                # Efficiency: inverse of tokens (fewer is better)
                avg_tokens = model_df['tokens_used'].mean() if 'tokens_used' in model_df else 100
                efficiency = min(100, (100 / avg_tokens) * 100) if avg_tokens > 0 else 0
                
                values = [pass_rate, avg_score, speed, efficiency]
                
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill='toself',
                    name=model
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                showlegend=True,
                title="Model Capabilities Comparison"
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    def render_agent_performance(self, df):
        """Render agent-specific performance view"""
        st.header("Agent Role Performance")
        
        if df.empty or 'agent_role' not in df:
            st.info("No agent role data to display")
            return
        
        selected_role = st.selectbox(
            "Select Agent Role",
            options=df['agent_role'].unique()
        )
        
        role_df = df[df['agent_role'] == selected_role]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Best model for this role
            if 'model' in role_df and 'score' in role_df:
                best_model = role_df.groupby('model')['score'].mean().idxmax()
                best_score = role_df.groupby('model')['score'].mean().max()
                
                st.info(f"**Best Model**: {best_model}")
                st.metric("Best Average Score", f"{best_score:.2f}")
        
        with col2:
            # Test category breakdown
            if 'test_category' in role_df:
                st.subheader("Performance by Test Category")
                category_scores = role_df.groupby('test_category')['score'].mean()
                
                fig = px.bar(
                    x=category_scores.values,
                    y=category_scores.index,
                    orientation='h',
                    title=f"{selected_role} - Category Performance",
                    labels={'x': 'Average Score', 'y': 'Test Category'},
                    color=category_scores.values,
                    color_continuous_scale='RdYlGn'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Model comparison for this role
        if 'model' in role_df:
            st.subheader(f"Model Comparison for {selected_role}")
            
            model_metrics = role_df.groupby('model').agg({
                'passed': 'mean',
                'score': 'mean',
                'execution_time': 'mean'
            }).reset_index()
            
            fig = make_subplots(
                rows=1, cols=3,
                subplot_titles=('Pass Rate', 'Average Score', 'Execution Time')
            )
            
            fig.add_trace(
                go.Bar(x=model_metrics['model'], y=model_metrics['passed'] * 100),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Bar(x=model_metrics['model'], y=model_metrics['score']),
                row=1, col=2
            )
            
            fig.add_trace(
                go.Bar(x=model_metrics['model'], y=model_metrics['execution_time']),
                row=1, col=3
            )
            
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    def render_detailed_analysis(self, df, comparisons):
        """Render detailed analysis view"""
        st.header("Detailed Analysis")
        
        # Test-level details
        st.subheader("Individual Test Results")
        
        if not df.empty:
            # Add filters
            col1, col2, col3 = st.columns(3)
            
            with col1:
                filter_model = st.selectbox(
                    "Filter by Model",
                    options=['All'] + list(df['model'].unique()) if 'model' in df else ['All']
                )
            
            with col2:
                filter_role = st.selectbox(
                    "Filter by Role",
                    options=['All'] + list(df['agent_role'].unique()) if 'agent_role' in df else ['All']
                )
            
            with col3:
                filter_passed = st.selectbox(
                    "Filter by Status",
                    options=['All', 'Passed', 'Failed']
                )
            
            # Apply filters
            filtered = df.copy()
            if filter_model != 'All':
                filtered = filtered[filtered['model'] == filter_model]
            if filter_role != 'All':
                filtered = filtered[filtered['agent_role'] == filter_role]
            if filter_passed == 'Passed':
                filtered = filtered[filtered['passed'] == True]
            elif filter_passed == 'Failed':
                filtered = filtered[filtered['passed'] == False]
            
            # Display filtered results
            st.dataframe(filtered, use_container_width=True)
            
            # Download button
            csv = filtered.to_csv(index=False)
            st.download_button(
                label="Download Filtered Results as CSV",
                data=csv,
                file_name=f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        # Comparison results
        if comparisons:
            st.subheader("Model Comparison Results")
            
            for comp in comparisons[-5:]:  # Show last 5 comparisons
                with st.expander(f"{comp['agent_role']} - {comp.get('test_time', 'Unknown time')}"):
                    st.json(comp)
    
    def render_test_runner(self):
        """Render test runner interface"""
        st.header("🔬 Run New A/B Test")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Test Configuration")
            
            # Model selection
            available_models = [
                "llama3.1:70b",
                "codellama:7b",
                "mistral:7b",
                "llama2:7b",
                "phi:latest",
                "neural-chat:7b",
                "gptFREE:latest",
                "gpt-oss:20b"
            ]
            
            selected_models = st.multiselect(
                "Select Models to Test",
                options=available_models,
                default=available_models[:2]
            )
            
            # Agent role selection
            agent_roles = [
                "backend_engineer",
                "frontend_developer",
                "data_scientist",
                "devops_engineer",
                "security_analyst",
                "project_manager",
                "compliance_officer"
            ]
            
            selected_role = st.selectbox(
                "Select Agent Role",
                options=agent_roles
            )
            
            # Test subset
            test_all = st.checkbox("Run All Tests", value=True)
            
            if not test_all:
                test_subset = st.text_input(
                    "Test IDs (comma-separated)",
                    placeholder="be_001,be_002,be_003"
                )
            else:
                test_subset = None
        
        with col2:
            st.subheader("Test Execution")
            
            if st.button("🚀 Run A/B Test", type="primary"):
                if not selected_models:
                    st.error("Please select at least one model")
                elif len(selected_models) < 2:
                    st.warning("Select at least 2 models for comparison")
                else:
                    st.info(f"Running A/B test for {selected_role} with models: {', '.join(selected_models)}")
                    
                    # Create command for running test
                    command = f"""
python -c "
from agents.app.testing.agent_model_ab_tester import AgentModelABTester
from agents.app.agents.enhanced_factory import EnhancedAgentFactory
import asyncio

async def run_test():
    tester = AgentModelABTester()
    factory = EnhancedAgentFactory()
    
    results = await tester.compare_models(
        models={selected_models},
        agent_role='{selected_role}',
        agent_factory=factory,
        test_subset={test_subset.split(',') if test_subset else None}
    )
    
    print('Test completed!')
    print(f'Winner: {{results.get(\\"winner\\")}}')
    
    report = tester.generate_report()
    print(report)

asyncio.run(run_test())
"
                    """
                    
                    st.code(command, language="python")
                    st.success("Test command generated! Run this in your terminal.")
            
            # Test status
            st.subheader("Recent Test Runs")
            
            # Check for recent results
            results_files = list(Path("test_results").glob("*.json"))
            if results_files:
                recent_files = sorted(results_files, key=lambda x: x.stat().st_mtime, reverse=True)[:5]
                
                for file in recent_files:
                    file_time = datetime.fromtimestamp(file.stat().st_mtime)
                    st.text(f"📄 {file.name} - {file_time.strftime('%Y-%m-%d %H:%M')}")
            else:
                st.info("No test results yet")

# Main execution
def main():
    dashboard = ABTestDashboard()
    dashboard.render_dashboard()

if __name__ == "__main__":
    main()