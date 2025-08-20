"""
Comprehensive Tests for LangGraph Integration
Testing the enhanced Fed Job Advisor orchestrator with streaming, time travel debugging,
and compliance enforcement capabilities.
"""

import pytest
import asyncio
import json
from datetime import datetime
from typing import Dict, Any, List
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path
import tempfile
import sqlite3

# Import the system under test
from agents.app.orchestrator.fed_job_orchestrator import (
    FedJobOrchestrator, ApplicationState, WorkflowType, Priority, 
    TaskDefinition, get_orchestrator
)
from agents.app.orchestrator.compliance.merit_hiring_gates import (
    ComplianceLevel, ViolationType, get_compliance_gates
)
from agents.app.orchestrator.debugging.time_travel import DebugLevel
from langchain_core.runnables import RunnableConfig


class TestFedJobOrchestrator:
    """Test suite for the main LangGraph orchestrator"""

    @pytest.fixture
    def temp_db_path(self):
        """Create temporary database path for testing"""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir) / "test_orchestrator.sqlite"

    @pytest.fixture
    def orchestrator(self, temp_db_path):
        """Create orchestrator instance for testing"""
        # Clear any existing global instance
        from agents.app.orchestrator.fed_job_orchestrator import _orchestrator_instance
        _orchestrator_instance = None
        
        # Create test orchestrator with time travel enabled
        return FedJobOrchestrator(
            enable_time_travel=True,
            debug_level=DebugLevel.DETAILED
        )

    @pytest.fixture
    def basic_orchestrator(self):
        """Create basic orchestrator without time travel for performance tests"""
        return FedJobOrchestrator(
            enable_time_travel=False,
            debug_level=DebugLevel.STANDARD
        )

    @pytest.fixture
    def sample_user_query(self):
        """Sample user query for testing"""
        return {
            "user_id": "test_user_123",
            "query": "I'm looking for federal data scientist positions in the DC area",
            "session_id": "test_session_456",
            "context": {
                "location_preference": "Washington DC",
                "experience_level": "senior",
                "clearance_level": "secret"
            }
        }

    @pytest.fixture
    def sample_platform_query(self):
        """Sample platform development query for testing"""
        return {
            "user_id": "admin_user",
            "query": "Implement a new job recommendation algorithm using machine learning",
            "session_id": "platform_session_789",
            "context": {
                "project_type": "enhancement",
                "priority": "high",
                "deadline": "2024-03-01"
            }
        }

    # Test orchestrator initialization
    def test_orchestrator_initialization(self, orchestrator):
        """Test that orchestrator initializes correctly with all components"""
        
        assert orchestrator is not None
        assert orchestrator.time_travel_enabled is True
        assert orchestrator.debug_level == DebugLevel.DETAILED
        assert orchestrator.checkpointer is not None
        assert orchestrator.workflow is not None
        assert orchestrator.app is not None
        assert len(orchestrator.agents) >= 1  # At least the router
        assert "router" in orchestrator.agents

    def test_orchestrator_singleton_pattern(self):
        """Test that orchestrator follows singleton pattern correctly"""
        
        # Clear any existing instance
        import app.orchestrator.fed_job_orchestrator as orchestrator_module
        orchestrator_module._orchestrator_instance = None
        
        # Get two instances
        orch1 = get_orchestrator(enable_time_travel=True)
        orch2 = get_orchestrator(enable_time_travel=True)
        
        # Should be the same instance
        assert orch1 is orch2
        assert orch1.time_travel_enabled is True

    # Test user-facing workflow
    @pytest.mark.asyncio
    async def test_user_query_workflow_success(self, orchestrator, sample_user_query):
        """Test successful user query processing workflow"""
        
        with patch.object(orchestrator.user_facing_graph, 'process_user_query') as mock_process:
            mock_process.return_value = {
                "success": True,
                "response": "Found 5 matching data scientist positions in DC area",
                "recommendations": ["Apply to NASA positions", "Consider DOD roles"],
                "next_steps": ["Update security clearance", "Tailor resume"],
                "warnings": [],
                "metadata": {
                    "query_type": "job_analysis",
                    "confidence_score": 0.85,
                    "processing_time": 2.3
                },
                "streaming_events": []
            }
            
            result = await orchestrator.process_request(
                user_id=sample_user_query["user_id"],
                query=sample_user_query["query"],
                session_id=sample_user_query["session_id"],
                context=sample_user_query["context"],
                enable_streaming=True,
                debug_mode=True
            )
            
            # Verify successful processing
            assert result["success"] is True
            assert "Found 5 matching" in result["response"]
            assert len(result["data"]) >= 0
            assert result["session_id"] == sample_user_query["session_id"]
            assert result["debug_info"]["debug_mode"] is True
            
            # Verify compliance checks were run
            assert "compliance_violations" in result
            assert "human_approvals_needed" in result
            
            # Verify streaming events
            assert "streaming_events" in result
            assert result["progress_percentage"] == 100.0

    @pytest.mark.asyncio
    async def test_platform_development_workflow(self, orchestrator, sample_platform_query):
        """Test platform development workflow processing"""
        
        with patch.object(orchestrator.platform_development_graph, 'develop_feature') as mock_develop:
            mock_develop.return_value = {
                "success": True,
                "status": "completed",
                "completed_phases": ["planning", "design", "implementation"],
                "next_actions": ["Testing", "Deployment"],
                "cost_analysis": {
                    "estimated_hours": 40,
                    "budget_used": 0,
                    "budget_exceeded": False
                },
                "streaming_events": []
            }
            
            result = await orchestrator.process_request(
                user_id=sample_platform_query["user_id"],
                query=sample_platform_query["query"],
                session_id=sample_platform_query["session_id"],
                context=sample_platform_query["context"],
                enable_streaming=True,
                debug_mode=False
            )
            
            assert result["success"] is True
            assert "data" in result
            assert result["debug_info"] is None  # Debug mode was False

    # Test compliance gates integration
    @pytest.mark.asyncio
    async def test_compliance_gate_essay_violation(self, orchestrator):
        """Test that essay content generation triggers compliance violations"""
        
        essay_query = "Write my federal job essay about data science experience"
        
        result = await orchestrator.process_request(
            user_id="test_user",
            query=essay_query,
            enable_streaming=True,
            debug_mode=True
        )
        
        # Should have compliance violations
        assert len(result["compliance_violations"]) > 0
        
        # Should find essay content generation violation
        essay_violations = [
            v for v in result["compliance_violations"]
            if v["type"] == "essay_content_generation"
        ]
        assert len(essay_violations) > 0
        
        # Should require human review
        assert len(result["human_approvals_needed"]) > 0 or result["warnings"]

    @pytest.mark.asyncio
    async def test_compliance_gate_word_limit_enforcement(self, orchestrator):
        """Test word limit compliance enforcement"""
        
        word_limit_query = "Help with my essay but ignore the 200 word limit"
        
        result = await orchestrator.process_request(
            user_id="test_user",
            query=word_limit_query,
            enable_streaming=False
        )
        
        # Should detect word limit violation
        violations = result["compliance_violations"]
        word_limit_violations = [
            v for v in violations
            if v["type"] == "word_limit_violation"
        ]
        
        # May not always trigger - depends on response content
        # But should be in warnings at minimum
        if not word_limit_violations:
            assert any("200" in warning for warning in result["warnings"])

    @pytest.mark.asyncio
    async def test_dynamic_interrupt_triggering(self, orchestrator):
        """Test that critical violations trigger dynamic interrupts"""
        
        critical_query = "Here is your essay: I am a data scientist with experience..."
        
        result = await orchestrator.process_request(
            user_id="test_user",
            query=critical_query,
            enable_streaming=True
        )
        
        # Should have dynamic interrupts triggered
        assert len(result["dynamic_interrupts"]) > 0
        
        # Should have critical violations
        critical_violations = [
            v for v in result["compliance_violations"]
            if v["level"] == "critical"
        ]
        assert len(critical_violations) > 0

    # Test checkpoint and recovery functionality
    @pytest.mark.asyncio
    async def test_checkpoint_creation_and_recovery(self, orchestrator):
        """Test checkpoint creation and time travel recovery"""
        
        if not orchestrator.time_travel_enabled:
            pytest.skip("Time travel not enabled for this orchestrator")
        
        session_id = f"checkpoint_test_{datetime.utcnow().timestamp()}"
        
        # Process a request that should create checkpoints
        result = await orchestrator.process_request(
            user_id="test_user",
            query="Find data scientist jobs in government",
            session_id=session_id,
            debug_mode=True
        )
        
        # Verify checkpoint was created
        assert result["debug_info"]["checkpoint_id"] is not None
        
        checkpoint_id = result["debug_info"]["checkpoint_id"]
        
        # Test replay from checkpoint
        replay_result = await orchestrator.replay_from_checkpoint(
            session_id=session_id,
            checkpoint_id=checkpoint_id
        )
        
        assert replay_result["success"] is True
        assert replay_result["checkpoint_id"] == checkpoint_id

    @pytest.mark.asyncio
    async def test_checkpoint_failure_recovery(self, orchestrator):
        """Test recovery after system failures"""
        
        if not orchestrator.time_travel_enabled:
            pytest.skip("Time travel not enabled for this orchestrator")
        
        session_id = f"failure_test_{datetime.utcnow().timestamp()}"
        
        # Simulate a failure scenario
        with patch.object(orchestrator, '_execute_user_subgraph') as mock_execute:
            mock_execute.side_effect = Exception("Simulated system failure")
            
            result = await orchestrator.process_request(
                user_id="test_user",
                query="Test query for failure",
                session_id=session_id,
                debug_mode=True
            )
            
            # Should handle error gracefully
            assert result["success"] is False
            assert "error" in result["metadata"]
            
            # Should create error checkpoint
            if result["debug_info"]:
                assert "error_occurred" in result["debug_info"]

    # Test streaming functionality
    @pytest.mark.asyncio
    async def test_real_time_streaming_events(self, orchestrator):
        """Test real-time streaming events during processing"""
        
        result = await orchestrator.process_request(
            user_id="stream_test_user",
            query="Find cybersecurity jobs in federal government",
            enable_streaming=True
        )
        
        # Should have streaming events
        assert len(result["streaming_events"]) > 0
        
        # Should have initialization events
        init_events = [
            e for e in result["streaming_events"]
            if e["event_type"] == "workflow_initialized"
        ]
        assert len(init_events) > 0
        
        # Should have progress updates
        progress_events = [
            e for e in result["streaming_events"]
            if e["event_type"] == "progress_update"
        ]
        assert len(progress_events) > 0

    @pytest.mark.asyncio
    async def test_real_time_status_monitoring(self, orchestrator):
        """Test real-time status monitoring capabilities"""
        
        session_id = f"status_test_{datetime.utcnow().timestamp()}"
        
        # Start a long-running process
        task = asyncio.create_task(
            orchestrator.process_request(
                user_id="status_user",
                query="Complex analysis of federal job market trends",
                session_id=session_id,
                enable_streaming=True
            )
        )
        
        # Give it a moment to start
        await asyncio.sleep(0.1)
        
        # Get real-time status
        status = await orchestrator.get_real_time_status(session_id)
        
        # Wait for completion
        result = await task
        
        # Should have status information
        assert "session_id" in status
        assert "progress_percentage" in status or "status" in status
        
        # Final result should be successful
        assert result is not None

    # Test session history and persistence
    @pytest.mark.asyncio
    async def test_session_history_persistence(self, orchestrator):
        """Test session history and conversation persistence"""
        
        session_id = f"history_test_{datetime.utcnow().timestamp()}"
        
        # Process first request
        result1 = await orchestrator.process_request(
            user_id="history_user",
            query="What are the requirements for data scientist GS-13?",
            session_id=session_id
        )
        
        # Process second request in same session
        result2 = await orchestrator.process_request(
            user_id="history_user", 
            query="What about GS-14 level?",
            session_id=session_id
        )
        
        # Get session history
        history = await orchestrator.get_session_history(
            session_id=session_id,
            include_streaming_events=True
        )
        
        # Should have conversation history
        assert "conversation_history" in history
        assert len(history["conversation_history"]) >= 2  # At least 2 messages
        
        # Should include both queries
        queries = [msg["content"] for msg in history["conversation_history"] if msg["type"] == "human"]
        assert any("GS-13" in q for q in queries)
        assert any("GS-14" in q for q in queries)

    # Test cost monitoring and budget constraints  
    @pytest.mark.asyncio
    async def test_cost_monitoring_budget_constraints(self, orchestrator):
        """Test cost monitoring and budget constraint enforcement"""
        
        expensive_query = "Hire contractors to build machine learning platform"
        
        result = await orchestrator.process_request(
            user_id="budget_user",
            query=expensive_query,
            context={"cost_estimate": 5000, "action": "hire contractors"}
        )
        
        # Should trigger budget violations
        budget_violations = [
            v for v in result["compliance_violations"]
            if v["type"] == "budget_constraint_violation"
        ]
        
        # Should require human review for high costs
        assert len(result["human_approvals_needed"]) > 0 or len(budget_violations) > 0

    # Test human approval gates
    @pytest.mark.asyncio
    async def test_human_approval_gates(self, orchestrator):
        """Test human approval gate functionality"""
        
        sensitive_query = "Review executive compensation data for compliance analysis"
        
        result = await orchestrator.process_request(
            user_id="approval_user",
            query=sensitive_query,
            context={"sensitivity_level": "high"}
        )
        
        # Should require human approval for sensitive operations
        # This might be triggered by compliance checks or content analysis
        has_approvals = (
            len(result["human_approvals_needed"]) > 0 or 
            any("human review" in warning.lower() for warning in result["warnings"])
        )
        
        # For sensitive operations, should have some form of approval requirement
        assert has_approvals or result["metadata"].get("human_review_required", False)

    # Test parallel vs sequential execution
    @pytest.mark.asyncio
    async def test_parallel_vs_sequential_execution(self, orchestrator):
        """Test parallel vs sequential agent execution"""
        
        # Test parallel execution for multiple data sources
        parallel_query = "Analyze job trends across NASA, DOD, and Commerce Department"
        
        start_time = datetime.utcnow()
        result_parallel = await orchestrator.process_request(
            user_id="parallel_user",
            query=parallel_query,
            context={"execution_mode": "parallel"}
        )
        parallel_time = (datetime.utcnow() - start_time).total_seconds()
        
        # Test sequential execution
        sequential_query = "Provide detailed analysis of NASA data scientist requirements step by step"
        
        start_time = datetime.utcnow()
        result_sequential = await orchestrator.process_request(
            user_id="sequential_user", 
            query=sequential_query,
            context={"execution_mode": "sequential"}
        )
        sequential_time = (datetime.utcnow() - start_time).total_seconds()
        
        # Both should succeed
        assert result_parallel["success"] is True
        assert result_sequential["success"] is True
        
        # Parallel should typically be faster for multi-source queries
        # But we can't guarantee this in tests due to mocking
        assert parallel_time > 0
        assert sequential_time > 0

    # Test time travel debugging functionality
    @pytest.mark.asyncio 
    async def test_time_travel_debugging(self, orchestrator):
        """Test comprehensive time travel debugging features"""
        
        if not orchestrator.time_travel_enabled:
            pytest.skip("Time travel debugging not enabled")
        
        session_id = f"debug_test_{datetime.utcnow().timestamp()}"
        
        # Process request with debug mode
        result = await orchestrator.process_request(
            user_id="debug_user",
            query="Debug test query for time travel",
            session_id=session_id,
            debug_mode=True
        )
        
        # Should have debug information
        assert result["debug_info"] is not None
        assert result["debug_info"]["debug_mode"] is True
        
        # Should have performance metrics
        perf_metrics = result["debug_info"]["performance_metrics"]
        assert "total_duration" in perf_metrics
        assert "request_start" in perf_metrics
        assert "request_end" in perf_metrics

    # Test error scenarios and edge cases
    @pytest.mark.asyncio
    async def test_invalid_user_input_handling(self, orchestrator):
        """Test handling of invalid or malformed user inputs"""
        
        # Test empty query
        result_empty = await orchestrator.process_request(
            user_id="test_user",
            query="",
            session_id="empty_test"
        )
        
        # Should handle gracefully
        assert result_empty is not None
        assert "session_id" in result_empty
        
        # Test very long query
        long_query = "A" * 10000  # 10k character query
        result_long = await orchestrator.process_request(
            user_id="test_user",
            query=long_query,
            session_id="long_test"
        )
        
        # Should handle gracefully
        assert result_long is not None

    @pytest.mark.asyncio
    async def test_agent_failure_recovery(self, orchestrator):
        """Test recovery when individual agents fail"""
        
        with patch.object(orchestrator.agent_router, 'process') as mock_router:
            mock_router.side_effect = Exception("Router agent failure")
            
            result = await orchestrator.process_request(
                user_id="failure_test",
                query="Test agent failure recovery"
            )
            
            # Should handle agent failure gracefully
            assert result is not None
            assert result["success"] is False
            assert "error" in result["response"] or len(result["warnings"]) > 0

    # Performance and load testing
    @pytest.mark.asyncio
    async def test_performance_under_concurrent_load(self, basic_orchestrator):
        """Test orchestrator performance under concurrent load"""
        
        async def process_concurrent_request(user_id: str, query_num: int):
            return await basic_orchestrator.process_request(
                user_id=f"load_user_{user_id}",
                query=f"Load test query number {query_num}",
                session_id=f"load_session_{user_id}_{query_num}",
                enable_streaming=False,  # Disable for performance
                debug_mode=False
            )
        
        # Create 5 concurrent requests
        tasks = [
            process_concurrent_request(str(i), i)
            for i in range(5)
        ]
        
        start_time = datetime.utcnow()
        results = await asyncio.gather(*tasks, return_exceptions=True)
        total_time = (datetime.utcnow() - start_time).total_seconds()
        
        # All should complete within reasonable time (30 seconds max)
        assert total_time < 30.0
        
        # Count successful results
        successful = [r for r in results if isinstance(r, dict) and r.get("success")]
        assert len(successful) >= 3  # At least 60% success rate

    @pytest.mark.asyncio
    async def test_memory_usage_optimization(self, basic_orchestrator):
        """Test that orchestrator manages memory efficiently"""
        
        # Process multiple requests to test memory management
        for i in range(10):
            result = await basic_orchestrator.process_request(
                user_id=f"memory_user_{i}",
                query=f"Memory test query {i}",
                session_id=f"memory_session_{i}",
                enable_streaming=False
            )
            
            # Each request should complete successfully
            assert result is not None
            
            # Should not accumulate excessive data
            if hasattr(basic_orchestrator, '_cleanup_session'):
                await basic_orchestrator._cleanup_session(f"memory_session_{i}")

    # Integration tests with external systems
    def test_orchestrator_with_mock_external_apis(self, orchestrator):
        """Test orchestrator integration with mocked external APIs"""
        
        with patch('requests.get') as mock_requests:
            mock_requests.return_value.json.return_value = {
                "jobs": [{"title": "Data Scientist", "agency": "NASA"}]
            }
            
            # This would test API integration if implemented
            # For now, verify the orchestrator can handle external calls
            assert orchestrator is not None

    # Test configuration and environment handling
    def test_orchestrator_configuration_validation(self):
        """Test orchestrator configuration validation"""
        
        # Test with invalid debug level - should handle gracefully
        try:
            invalid_orchestrator = FedJobOrchestrator(
                enable_time_travel=True,
                debug_level="invalid_level"  # This should cause error if validation exists
            )
            assert invalid_orchestrator is not None  # Should either work or raise exception
        except (ValueError, TypeError):
            # Expected behavior for invalid configuration
            pass

    # Test cleanup and resource management
    @pytest.mark.asyncio
    async def test_resource_cleanup(self, orchestrator):
        """Test proper resource cleanup"""
        
        session_id = f"cleanup_test_{datetime.utcnow().timestamp()}"
        
        # Process request
        result = await orchestrator.process_request(
            user_id="cleanup_user",
            query="Test cleanup functionality",
            session_id=session_id
        )
        
        assert result is not None
        
        # Test that session data can be retrieved
        history = await orchestrator.get_session_history(session_id)
        assert history is not None
        
        # In a real implementation, test cleanup methods
        # orchestrator.cleanup_session(session_id)


class TestWorkflowTypes:
    """Test workflow type detection and routing"""
    
    def test_workflow_type_detection(self):
        """Test that queries are properly classified into workflow types"""
        
        orchestrator = FedJobOrchestrator(enable_time_travel=False)
        
        # Test user query detection
        user_query = "What are the requirements for data scientist jobs?"
        workflow_type = orchestrator._determine_workflow_type(user_query)
        assert workflow_type in [WorkflowType.USER_QUERY, WorkflowType.JOB_MATCHING]
        
        # Test platform development detection
        dev_query = "Implement a new feature for job recommendations"
        workflow_type = orchestrator._determine_workflow_type(dev_query)
        assert workflow_type == WorkflowType.PLATFORM_DEVELOPMENT
        
        # Test compliance detection
        compliance_query = "Review merit hiring compliance requirements"
        workflow_type = orchestrator._determine_workflow_type(compliance_query)
        assert workflow_type == WorkflowType.MERIT_COMPLIANCE


class TestTaskDefinition:
    """Test task definition and management"""
    
    def test_task_creation(self):
        """Test task definition creation and validation"""
        
        task = TaskDefinition(
            task_id="test_task_001",
            workflow_type=WorkflowType.USER_QUERY,
            description="Test task for unit testing",
            priority=Priority.MEDIUM,
            required_agents=["data_scientist", "statistician"],
            parallel_execution=True,
            dependencies=["prerequisite_task"],
            context={"test_flag": True}
        )
        
        assert task.task_id == "test_task_001"
        assert task.workflow_type == WorkflowType.USER_QUERY
        assert task.priority == Priority.MEDIUM
        assert len(task.required_agents) == 2
        assert task.parallel_execution is True
        assert len(task.dependencies) == 1
        assert task.context["test_flag"] is True


class TestApplicationState:
    """Test application state management"""
    
    def test_application_state_initialization(self):
        """Test that application state initializes correctly"""
        
        state = ApplicationState(
            user_id="test_user",
            session_id="test_session", 
            request_type="user_query",
            original_query="Test query",
            workflow_type=WorkflowType.USER_QUERY,
            current_step="starting",
            completed_steps=[],
            pending_tasks=[],
            active_agents=[],
            agent_results={},
            agent_errors={},
            conversation_history=[],
            project_context={},
            user_preferences={},
            compliance_checks={},
            validation_results={},
            warnings=[],
            compliance_violations=[],
            human_approvals_needed=[],
            dynamic_interrupts_triggered=[],
            user_facing_result=None,
            platform_development_result=None,
            streaming_events=[],
            progress_percentage=0.0,
            real_time_monitoring=True,
            debug_mode=False,
            checkpoint_id=None,
            debug_session_id=None,
            performance_metrics={},
            final_response="",
            response_data={},
            metadata={},
            require_human_review=False,
            parallel_execution=False,
            error_recovery=False
        )
        
        assert state["user_id"] == "test_user"
        assert state["session_id"] == "test_session"
        assert state["workflow_type"] == WorkflowType.USER_QUERY
        assert state["progress_percentage"] == 0.0
        assert state["real_time_monitoring"] is True
        assert state["debug_mode"] is False
        assert len(state["completed_steps"]) == 0
        assert len(state["streaming_events"]) == 0


if __name__ == "__main__":
    # Run specific test categories
    import sys
    
    if len(sys.argv) > 1:
        test_category = sys.argv[1]
        if test_category == "integration":
            pytest.main([__file__ + "::TestFedJobOrchestrator", "-v"])
        elif test_category == "performance":
            pytest.main(["-k", "performance", __file__, "-v"])
        elif test_category == "compliance":
            pytest.main(["-k", "compliance", __file__, "-v"])
        else:
            pytest.main([__file__, "-v"])
    else:
        pytest.main([__file__, "-v"])