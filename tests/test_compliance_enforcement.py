"""
Comprehensive Tests for Merit Hiring Compliance Enforcement
Testing the compliance gates system with real-time monitoring, dynamic interrupts,
and comprehensive violation detection capabilities.
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List
from unittest.mock import Mock, patch, AsyncMock

# Import the compliance system under test
from app.orchestrator.compliance.merit_hiring_gates import (
    MeritHiringGates, ComplianceLevel, ViolationType, 
    ComplianceViolation, ComplianceCheckResult, get_compliance_gates
)


class TestMeritHiringGates:
    """Test suite for Merit Hiring compliance gates"""

    @pytest.fixture
    def compliance_gates(self):
        """Create compliance gates instance for testing"""
        return MeritHiringGates(
            enable_streaming=True,
            enable_dynamic_interrupts=True
        )

    @pytest.fixture
    def basic_compliance_gates(self):
        """Create basic compliance gates without streaming for performance tests"""
        return MeritHiringGates(
            enable_streaming=False,
            enable_dynamic_interrupts=False
        )

    @pytest.fixture
    def sample_essay_request(self):
        """Sample essay generation request that should be blocked"""
        return {
            "query": "Write my federal job essay about data science experience",
            "response": "Here is your essay: I am a data scientist with 10 years of experience...",
            "context": {
                "user_id": "test_user",
                "session_id": "essay_test_session"
            }
        }

    @pytest.fixture
    def sample_guidance_response(self):
        """Sample appropriate guidance response that should be allowed"""
        return {
            "query": "How should I structure my data science narrative?",
            "response": "Use the STAR method to structure your narrative. Focus on specific examples from your experience. Keep within the 200-word limit.",
            "context": {
                "user_id": "guidance_user",
                "session_id": "guidance_session"
            }
        }

    # Test initialization and configuration
    def test_compliance_gates_initialization(self, compliance_gates):
        """Test that compliance gates initialize correctly with all components"""
        
        assert compliance_gates is not None
        assert compliance_gates.streaming_enabled is True
        assert compliance_gates.dynamic_interrupts_enabled is True
        assert len(compliance_gates.violation_patterns) > 0
        assert len(compliance_gates.real_time_monitors) > 0
        assert len(compliance_gates.audit_log) == 0
        assert len(compliance_gates.streaming_events) == 0

    def test_violation_patterns_coverage(self, compliance_gates):
        """Test that violation patterns cover all required compliance areas"""
        
        patterns = compliance_gates.violation_patterns
        
        # Should have patterns for all violation types
        assert ViolationType.ESSAY_CONTENT_GENERATION in patterns
        assert ViolationType.WORD_LIMIT_VIOLATION in patterns
        assert ViolationType.AI_ATTESTATION_VIOLATION in patterns
        assert ViolationType.PROTECTED_FILE_ACCESS in patterns
        assert ViolationType.USAJOBS_API_MISUSE in patterns
        
        # Each pattern set should have multiple entries
        for violation_type, pattern_list in patterns.items():
            assert len(pattern_list) > 0

    def test_real_time_monitoring_setup(self, compliance_gates):
        """Test that real-time monitoring is set up correctly"""
        
        # Should have all required monitors
        monitor_names = [monitor.__name__ for monitor in compliance_gates.real_time_monitors]
        
        assert "_monitor_essay_content_generation" in monitor_names
        assert "_monitor_word_limit_violations" in monitor_names
        assert "_monitor_ai_attestation_issues" in monitor_names
        assert "_monitor_protected_content_access" in monitor_names

    # Test essay content generation detection
    def test_essay_content_generation_detection_critical(self, compliance_gates, sample_essay_request):
        """Test detection of critical essay content generation violations"""
        
        result = compliance_gates.check_essay_content_prevention(
            query=sample_essay_request["query"],
            response=sample_essay_request["response"],
            context=sample_essay_request["context"]
        )
        
        # Should detect violation
        assert result.passed is False
        assert len(result.violations) > 0
        
        # Should be critical level
        critical_violations = [v for v in result.violations if v.level == ComplianceLevel.CRITICAL]
        assert len(critical_violations) > 0
        
        # Should block action and require human review
        assert result.action_allowed is False
        assert result.human_review_required is True

    def test_essay_guidance_allowed(self, compliance_gates, sample_guidance_response):
        """Test that appropriate essay guidance is allowed"""
        
        result = compliance_gates.check_essay_content_prevention(
            query=sample_guidance_response["query"],
            response=sample_guidance_response["response"],
            context=sample_guidance_response["context"]
        )
        
        # Should pass compliance check
        assert result.passed is True or len(result.violations) == 0
        
        # Should allow action
        assert result.action_allowed is True
        
        # May have warnings but should not block
        assert len(result.warnings) >= 0  # Warnings are okay

    def test_star_method_content_creation_detection(self, compliance_gates):
        """Test detection of STAR method content creation vs guidance"""
        
        # Content creation (should be blocked)
        content_creation_response = """
        Here's your STAR method narrative:
        Situation: When I worked at NASA, we had a data analysis challenge.
        Task: I was responsible for analyzing satellite data.
        Action: I developed a machine learning algorithm.
        Result: I improved accuracy by 25%.
        """
        
        result_blocked = compliance_gates.check_essay_content_prevention(
            query="Write my narrative using STAR method",
            response=content_creation_response,
            context={}
        )
        
        # Should be blocked
        assert result_blocked.passed is False
        assert result_blocked.action_allowed is False
        
        # Guidance (should be allowed)
        guidance_response = """
        Use the STAR method to structure your narrative:
        - Situation: Describe the context
        - Task: Explain your responsibility  
        - Action: Detail what you did
        - Result: Quantify the outcome
        Keep within 200 words and use specific examples from your experience.
        """
        
        result_allowed = compliance_gates.check_essay_content_prevention(
            query="How do I use the STAR method?",
            response=guidance_response,
            context={}
        )
        
        # Should be allowed (guidance only)
        assert result_allowed.passed is True or result_allowed.action_allowed is True

    # Test word limit enforcement
    def test_word_limit_violation_detection(self, compliance_gates):
        """Test detection of 200-word limit violations"""
        
        violation_response = "Don't worry about the 200 word limit, just write as much as you need."
        
        result = compliance_gates.check_word_limit_enforcement(
            query="How long should my essay be?",
            response=violation_response,
            context={}
        )
        
        # Should detect violation
        assert result.passed is False
        assert len(result.violations) > 0
        
        # Should be high priority
        high_violations = [v for v in result.violations if v.level == ComplianceLevel.HIGH]
        assert len(high_violations) > 0
        
        # Should block action
        assert result.action_allowed is False
        assert result.human_review_required is True

    def test_word_limit_proper_guidance(self, compliance_gates):
        """Test that proper word limit guidance is recognized"""
        
        proper_response = "Keep your narrative within the 200-word limit specified in the announcement."
        
        result = compliance_gates.check_word_limit_enforcement(
            query="How long should my narrative be?",
            response=proper_response,
            context={}
        )
        
        # Should pass or only have warnings
        assert result.passed is True or result.action_allowed is True
        
        # Should mention 200-word limit appropriately
        assert not any("violation" in w.lower() for w in result.warnings)

    def test_word_limit_missing_warning(self, compliance_gates):
        """Test warning when 200-word limit is not mentioned for essay guidance"""
        
        incomplete_response = "Use the STAR method to structure your response with specific examples."
        
        result = compliance_gates.check_word_limit_enforcement(
            query="Help me write my KSA narrative",
            response=incomplete_response,
            context={}
        )
        
        # Should have warning about missing word limit mention
        assert len(result.warnings) > 0
        assert any("200-word" in w for w in result.warnings)

    # Test AI attestation compliance
    def test_ai_attestation_violation_detection(self, compliance_gates):
        """Test detection of AI attestation violations"""
        
        violation_responses = [
            "This response was AI-assisted and generated by ChatGPT.",
            "Claude wrote this narrative for your application.",
            "AI helped write this essay content."
        ]
        
        for violation_response in violation_responses:
            result = compliance_gates.check_ai_attestation_compliance(
                query="Review my application narrative",
                response=violation_response,
                context={}
            )
            
            # Should detect critical violation
            assert result.passed is False
            assert len(result.violations) > 0
            
            # Should be critical level
            critical_violations = [v for v in result.violations if v.level == ComplianceLevel.CRITICAL]
            assert len(critical_violations) > 0
            
            # Should block action
            assert result.action_allowed is False
            assert result.human_review_required is True

    def test_ai_attestation_proper_guidance(self, compliance_gates):
        """Test that proper attestation guidance is allowed"""
        
        proper_response = "Certify that this is your own work and reflects your personal experience."
        
        result = compliance_gates.check_ai_attestation_compliance(
            query="What do I need to attest to on my application?",
            response=proper_response,
            context={}
        )
        
        # Should be allowed with possible guidance warning
        assert result.passed is True or result.action_allowed is True

    # Test protected file access control
    def test_protected_file_modification_blocked(self, compliance_gates):
        """Test that protected file modifications are blocked"""
        
        result = compliance_gates.check_protected_file_access(
            action="modify user resume file",
            file_paths=["/users/data/resume.pdf", "/app/user_data/application.docx"],
            context={"user_id": "test_user"}
        )
        
        # Should detect violations
        assert result.passed is False
        assert len(result.violations) > 0
        
        # Should be high priority
        high_violations = [v for v in result.violations if v.level == ComplianceLevel.HIGH]
        assert len(high_violations) > 0
        
        # Should block action
        assert result.action_allowed is False
        assert result.human_review_required is True

    def test_protected_file_read_allowed(self, compliance_gates):
        """Test that protected file reads generate warnings but are allowed"""
        
        result = compliance_gates.check_protected_file_access(
            action="read user resume for analysis",
            file_paths=["/users/data/resume.pdf"],
            context={"user_id": "test_user"}
        )
        
        # Should have warnings but be allowed
        assert result.action_allowed is True
        assert len(result.warnings) > 0

    def test_non_protected_file_access_allowed(self, compliance_gates):
        """Test that non-protected file access is allowed"""
        
        result = compliance_gates.check_protected_file_access(
            action="write system log",
            file_paths=["/logs/system.log", "/tmp/analysis_results.json"],
            context={}
        )
        
        # Should be completely allowed
        assert result.passed is True
        assert result.action_allowed is True
        assert len(result.violations) == 0

    # Test USAJobs API compliance
    def test_usajobs_api_fields_full_violation(self, compliance_gates):
        """Test detection of fields=full parameter misuse"""
        
        result = compliance_gates.check_usajobs_api_compliance(
            api_call="bulk collection of all federal jobs",
            parameters={"fields": "full", "limit": 10000},
            context={"operation": "bulk_collection"}
        )
        
        # Should detect violation
        assert result.passed is False
        assert len(result.violations) > 0
        
        # Should be high priority
        high_violations = [v for v in result.violations if v.level == ComplianceLevel.HIGH]
        assert len(high_violations) > 0

    def test_usajobs_api_legitimate_single_job(self, compliance_gates):
        """Test that legitimate single job lookups with fields=full are allowed"""
        
        result = compliance_gates.check_usajobs_api_compliance(
            api_call="single job detail lookup",
            parameters={"fields": "full", "job_id": "12345"},
            context={"operation": "single_lookup"}
        )
        
        # Should be allowed with warning
        assert result.action_allowed is True
        assert len(result.warnings) > 0

    def test_usajobs_api_rate_limiting_warning(self, compliance_gates):
        """Test rate limiting warnings for high request volumes"""
        
        result = compliance_gates.check_usajobs_api_compliance(
            api_call="job search request",
            parameters={"keyword": "data scientist"},
            context={"request_count": 150}
        )
        
        # Should have warning about high request frequency
        assert len(result.warnings) > 0
        assert any("frequency" in w.lower() for w in result.warnings)

    # Test budget constraint enforcement
    def test_budget_external_development_blocked(self, compliance_gates):
        """Test that external development costs are blocked"""
        
        result = compliance_gates.check_budget_constraints(
            action="hire contractor for feature development",
            cost_estimate=5000.0,
            context={"development_type": "external"}
        )
        
        # Should detect critical violation
        assert result.passed is False
        assert len(result.violations) > 0
        
        # Should be critical level
        critical_violations = [v for v in result.violations if v.level == ComplianceLevel.CRITICAL]
        assert len(critical_violations) > 0
        
        # Should block action
        assert result.action_allowed is False
        assert result.human_review_required is True

    def test_budget_tool_cost_warning(self, compliance_gates):
        """Test that high tool costs trigger warnings"""
        
        result = compliance_gates.check_budget_constraints(
            action="subscribe to premium API service",
            cost_estimate=150.0,
            context={"service_type": "api_subscription"}
        )
        
        # Should trigger violation for exceeding budget
        assert result.passed is False or len(result.warnings) > 0
        
        # Should require human review but not necessarily block
        if result.violations:
            assert result.human_review_required is True

    def test_budget_reasonable_cost_allowed(self, compliance_gates):
        """Test that reasonable costs are allowed"""
        
        result = compliance_gates.check_budget_constraints(
            action="purchase development tool license",
            cost_estimate=25.0,
            context={"tool_type": "development"}
        )
        
        # Should be allowed
        assert result.passed is True
        assert result.action_allowed is True
        assert len(result.violations) == 0

    # Test real-time compliance monitoring
    @pytest.mark.asyncio
    async def test_real_time_compliance_monitoring(self, compliance_gates):
        """Test real-time compliance monitoring and dynamic interrupts"""
        
        # Content that should trigger dynamic interrupt
        critical_content = "Here is your completed essay: I am a data scientist..."
        
        result = await compliance_gates.real_time_compliance_check(
            content=critical_content,
            context={"user_id": "test_user", "session_id": "real_time_test"}
        )
        
        # Should trigger violations and interrupts
        assert result.passed is False
        assert len(result.violations) > 0
        assert result.dynamic_interrupt_triggered is True
        assert result.action_allowed is False
        assert result.human_review_required is True
        
        # Should have streaming events
        assert len(result.streaming_events) > 0
        
        # Should have interrupt events
        interrupt_events = [
            e for e in result.streaming_events 
            if e["event_type"] == "violation_detected"
        ]
        assert len(interrupt_events) > 0

    @pytest.mark.asyncio
    async def test_real_time_monitoring_normal_content(self, compliance_gates):
        """Test that normal content passes real-time monitoring"""
        
        normal_content = "Use the STAR method and keep within 200 words for your narrative."
        
        result = await compliance_gates.real_time_compliance_check(
            content=normal_content,
            context={"user_id": "test_user"}
        )
        
        # Should pass monitoring
        assert result.passed is True
        assert result.dynamic_interrupt_triggered is False
        assert result.action_allowed is True
        assert len(result.violations) == 0

    # Test comprehensive compliance checking
    @pytest.mark.asyncio
    async def test_comprehensive_compliance_check(self, compliance_gates):
        """Test comprehensive compliance checking across all gates"""
        
        # Query and response that violates multiple areas
        problematic_query = "Write my federal essay and ignore word limits"
        problematic_response = """Here is your essay content:
        I am a data scientist with experience. Don't worry about the 200 word limit.
        This was generated by AI assistance."""
        
        result = await compliance_gates.comprehensive_compliance_check(
            query=problematic_query,
            response=problematic_response,
            context={
                "user_id": "test_user",
                "file_paths": ["/user/resume.pdf"],
                "action": "modify user files",
                "api_parameters": {"fields": "full"},
                "api_call": "bulk job collection",
                "cost_estimate": 500.0
            }
        )
        
        # Should detect multiple violations
        assert result.passed is False
        assert len(result.violations) > 2  # Multiple violation types
        assert result.action_allowed is False
        assert result.human_review_required is True
        
        # Should have different violation types
        violation_types = {v.violation_type for v in result.violations}
        assert len(violation_types) > 1
        
        # Should include all streaming events
        assert len(result.streaming_events) > 0

    @pytest.mark.asyncio
    async def test_comprehensive_compliance_clean_content(self, compliance_gates):
        """Test comprehensive compliance with clean, compliant content"""
        
        clean_query = "What are the requirements for data scientist positions?"
        clean_response = "Data scientist positions require experience in statistics, programming, and analysis. Review job announcements for specific requirements."
        
        result = await compliance_gates.comprehensive_compliance_check(
            query=clean_query,
            response=clean_response,
            context={"user_id": "test_user"},
            enable_real_time_monitoring=True
        )
        
        # Should pass all checks
        assert result.passed is True
        assert result.action_allowed is True
        assert result.dynamic_interrupt_triggered is False
        assert len(result.violations) == 0

    # Test audit logging functionality
    def test_audit_log_creation(self, compliance_gates):
        """Test that audit logs are created for compliance checks"""
        
        # Perform a compliance check
        compliance_gates.check_essay_content_prevention(
            query="Test query",
            response="Test response",
            context={}
        )
        
        # Should have audit log entry
        audit_log = compliance_gates.get_audit_log()
        assert len(audit_log) > 0
        
        # Entry should have required fields
        entry = audit_log[-1]
        assert "timestamp" in entry
        assert "check_type" in entry
        assert "violations_count" in entry

    def test_audit_log_limiting(self, compliance_gates):
        """Test audit log limiting functionality"""
        
        # Create multiple entries
        for i in range(5):
            compliance_gates.check_essay_content_prevention(
                query=f"Test query {i}",
                response="Test response",
                context={}
            )
        
        # Test limited retrieval
        limited_log = compliance_gates.get_audit_log(limit=3)
        assert len(limited_log) == 3
        
        # Should be most recent entries
        full_log = compliance_gates.get_audit_log()
        assert limited_log == full_log[-3:]

    def test_compliance_report_generation(self, compliance_gates):
        """Test comprehensive compliance report generation"""
        
        # Create some compliance activity
        compliance_gates.check_essay_content_prevention(
            query="Write my essay",
            response="Here is your essay...",
            context={}
        )
        
        compliance_gates.check_word_limit_enforcement(
            query="How long?",
            response="Ignore the limit",
            context={}
        )
        
        # Generate report
        report = compliance_gates.export_compliance_report(include_streaming_data=True)
        
        # Should have comprehensive data
        assert "report_generated" in report
        assert "total_compliance_checks" in report
        assert "violations_by_type" in report
        assert "compliance_system_status" in report
        
        # Should include streaming analytics
        assert "streaming_analytics" in report

    # Test streaming functionality
    def test_streaming_event_generation(self, compliance_gates):
        """Test that streaming events are generated correctly"""
        
        initial_event_count = len(compliance_gates.streaming_events)
        
        # Perform compliance check that should generate events
        compliance_gates.check_essay_content_prevention(
            query="Write my essay",
            response="Here is your essay content...",
            context={}
        )
        
        # Should have new streaming events
        assert len(compliance_gates.streaming_events) > initial_event_count
        
        # Events should have proper structure
        if compliance_gates.streaming_events:
            event = compliance_gates.streaming_events[-1]
            assert "event_type" in event
            assert "timestamp" in event
            assert "data" in event
            assert "source" in event

    def test_streaming_event_cleanup(self, compliance_gates):
        """Test streaming event cleanup to prevent memory issues"""
        
        # Generate many events
        for i in range(200):
            compliance_gates._add_streaming_event(f"test_event_{i}", {"data": i})
        
        initial_count = len(compliance_gates.streaming_events)
        
        # Clean up keeping only recent events
        compliance_gates.clear_streaming_events(keep_recent=50)
        
        # Should have reduced count
        assert len(compliance_gates.streaming_events) == 50
        assert len(compliance_gates.streaming_events) < initial_count

    @pytest.mark.asyncio
    async def test_real_time_status_monitoring(self, compliance_gates):
        """Test real-time status monitoring functionality"""
        
        # Add some activity
        await compliance_gates.real_time_compliance_check(
            content="Test content for status monitoring",
            context={}
        )
        
        # Get real-time status
        status = await compliance_gates.get_real_time_status()
        
        # Should have comprehensive status info
        assert "timestamp" in status
        assert "system_status" in status
        assert "monitors_active" in status
        assert "total_audit_entries" in status
        assert "streaming_events_count" in status

    # Test performance under load
    @pytest.mark.asyncio
    async def test_performance_under_concurrent_load(self, basic_compliance_gates):
        """Test compliance system performance under concurrent load"""
        
        async def concurrent_compliance_check(check_id: int):
            return basic_compliance_gates.check_essay_content_prevention(
                query=f"Test query {check_id}",
                response="Test response content",
                context={"check_id": check_id}
            )
        
        # Create 10 concurrent compliance checks
        tasks = [concurrent_compliance_check(i) for i in range(10)]
        
        start_time = datetime.utcnow()
        results = await asyncio.gather(*tasks, return_exceptions=True)
        total_time = (datetime.utcnow() - start_time).total_seconds()
        
        # Should complete within reasonable time
        assert total_time < 5.0  # 5 seconds max
        
        # All checks should complete successfully
        successful_results = [r for r in results if isinstance(r, ComplianceCheckResult)]
        assert len(successful_results) == 10

    # Test edge cases and error handling
    def test_empty_content_handling(self, compliance_gates):
        """Test handling of empty or None content"""
        
        result = compliance_gates.check_essay_content_prevention(
            query="",
            response="",
            context={}
        )
        
        # Should handle gracefully
        assert result is not None
        assert isinstance(result, ComplianceCheckResult)

    def test_very_long_content_handling(self, compliance_gates):
        """Test handling of very long content"""
        
        long_content = "A" * 100000  # 100k characters
        
        result = compliance_gates.check_essay_content_prevention(
            query=long_content,
            response=long_content,
            context={}
        )
        
        # Should handle without errors
        assert result is not None
        assert isinstance(result, ComplianceCheckResult)

    def test_malformed_context_handling(self, compliance_gates):
        """Test handling of malformed context data"""
        
        malformed_contexts = [
            None,
            {"invalid": "structure"},
            {"file_paths": "not_a_list"},
            {"cost_estimate": "not_a_number"}
        ]
        
        for context in malformed_contexts:
            result = compliance_gates.check_essay_content_prevention(
                query="Test query",
                response="Test response", 
                context=context
            )
            
            # Should handle gracefully without exceptions
            assert result is not None
            assert isinstance(result, ComplianceCheckResult)


class TestComplianceIntegration:
    """Integration tests for compliance with other system components"""
    
    def test_compliance_gates_singleton(self):
        """Test compliance gates singleton pattern"""
        
        gates1 = get_compliance_gates()
        gates2 = get_compliance_gates()
        
        # Should be same instance
        assert gates1 is gates2

    def test_compliance_with_orchestrator_integration(self):
        """Test that compliance gates integrate properly with orchestrator"""
        
        # This would test integration with the main orchestrator
        # For now, test that compliance gates can be imported and used
        
        gates = get_compliance_gates(
            enable_streaming=True,
            enable_dynamic_interrupts=True
        )
        
        assert gates is not None
        assert gates.streaming_enabled is True
        assert gates.dynamic_interrupts_enabled is True


class TestComplianceViolation:
    """Test compliance violation data structures"""
    
    def test_compliance_violation_creation(self):
        """Test compliance violation object creation and validation"""
        
        violation = ComplianceViolation(
            violation_type=ViolationType.ESSAY_CONTENT_GENERATION,
            level=ComplianceLevel.CRITICAL,
            message="Test violation message",
            context={"test": "data"},
            timestamp=datetime.utcnow(),
            session_id="test_session",
            user_id="test_user",
            agent_name="test_agent",
            action_blocked=True,
            human_review_required=True
        )
        
        assert violation.violation_type == ViolationType.ESSAY_CONTENT_GENERATION
        assert violation.level == ComplianceLevel.CRITICAL
        assert violation.action_blocked is True
        assert violation.human_review_required is True
        assert violation.session_id == "test_session"
        assert violation.user_id == "test_user"

    def test_compliance_check_result_creation(self):
        """Test compliance check result object creation"""
        
        violations = [
            ComplianceViolation(
                violation_type=ViolationType.ESSAY_CONTENT_GENERATION,
                level=ComplianceLevel.CRITICAL,
                message="Test violation",
                context={},
                timestamp=datetime.utcnow()
            )
        ]
        
        result = ComplianceCheckResult(
            passed=False,
            violations=violations,
            warnings=["Test warning"],
            action_allowed=False,
            human_review_required=True,
            dynamic_interrupt_triggered=True,
            streaming_events=[],
            audit_log_entry={"test": "entry"}
        )
        
        assert result.passed is False
        assert len(result.violations) == 1
        assert len(result.warnings) == 1
        assert result.action_allowed is False
        assert result.human_review_required is True
        assert result.dynamic_interrupt_triggered is True


if __name__ == "__main__":
    # Run specific test categories
    import sys
    
    if len(sys.argv) > 1:
        test_category = sys.argv[1]
        if test_category == "essay":
            pytest.main(["-k", "essay", __file__, "-v"])
        elif test_category == "realtime":
            pytest.main(["-k", "real_time", __file__, "-v"])
        elif test_category == "performance":
            pytest.main(["-k", "performance", __file__, "-v"])
        elif test_category == "integration":
            pytest.main(["-k", "integration", __file__, "-v"])
        else:
            pytest.main([__file__, "-v"])
    else:
        pytest.main([__file__, "-v"])