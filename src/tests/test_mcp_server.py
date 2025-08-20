"""
Test MCP Server Functionality
"""

import pytest
import asyncio
import json
from unittest.mock import AsyncMock, patch

# Add src to path for imports
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.mcp_server import FedJobAdvisorMCP

@pytest.fixture
def mcp_server():
    """Create MCP server instance for testing"""
    return FedJobAdvisorMCP()

class TestMCPServer:
    """Test MCP server functionality"""
    
    def test_server_initialization(self, mcp_server):
        """Test MCP server initializes correctly"""
        assert mcp_server.agent_base_url == "http://localhost:8001"
        assert mcp_server.server is not None
        assert len(mcp_server.agent_tools) > 0
        
    def test_agent_tools_registered(self, mcp_server):
        """Test all agent tools are registered"""
        expected_tools = [
            "analyze_data_scientist_profile",
            "analyze_statistician_profile", 
            "analyze_database_admin_profile",
            "analyze_devops_profile",
            "analyze_it_specialist_profile",
            "check_essay_compliance",
            "analyze_resume_compression",
            "research_executive_orders",
            "analyze_job_market",
            "orchestrate_job_collection",
            "route_to_best_agent"
        ]
        
        for tool in expected_tools:
            assert tool in mcp_server.agent_tools
            
    def test_tool_schemas(self, mcp_server):
        """Test tool schemas are properly defined"""
        for tool_name, config in mcp_server.agent_tools.items():
            assert "description" in config
            assert "agent_role" in config
            assert "endpoint" in config
            assert "schema" in config
            
            schema = config["schema"]
            assert "type" in schema
            assert schema["type"] == "object"
            assert "properties" in schema
            assert "user_id" in schema["properties"]
            
    @pytest.mark.asyncio
    async def test_agent_call_invalid_tool(self, mcp_server):
        """Test calling invalid tool returns error"""
        result = await mcp_server._call_agent("invalid_tool", {})
        assert len(result) == 1
        assert "Unknown agent tool" in result[0].text
        
    @pytest.mark.asyncio
    @patch('httpx.AsyncClient')
    async def test_agent_call_success(self, mock_client, mcp_server):
        """Test successful agent call"""
        # Mock successful health check
        mock_health_response = AsyncMock()
        mock_health_response.status_code = 200
        
        # Mock successful agent response
        mock_agent_response = AsyncMock()
        mock_agent_response.status_code = 200
        mock_agent_response.json.return_value = {
            "success": True,
            "message": "Analysis completed",
            "data": {
                "score": "Excellent",
                "recommendations": {
                    "skills": ["Improve Python skills"]
                }
            }
        }
        
        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_health_response
        mock_client_instance.post.return_value = mock_agent_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance
        
        result = await mcp_server._call_agent("analyze_data_scientist_profile", {
            "user_id": "test_user",
            "skills": ["Python"],
            "experience": "5 years"
        })
        
        assert len(result) == 1
        assert "Analysis completed" in result[0].text
        assert "Excellent" in result[0].text
        
    @pytest.mark.asyncio
    @patch('httpx.AsyncClient')
    async def test_agent_service_not_running(self, mock_client, mcp_server):
        """Test when agent service is not running"""
        # Mock connection error
        mock_client_instance = AsyncMock()
        mock_client_instance.get.side_effect = Exception("Connection refused")
        mock_client.return_value.__aenter__.return_value = mock_client_instance
        
        result = await mcp_server._call_agent("analyze_data_scientist_profile", {
            "user_id": "test_user"
        })
        
        assert len(result) == 1
        assert "Cannot connect to agent service" in result[0].text or "Unexpected error" in result[0].text

if __name__ == "__main__":
    pytest.main([__file__])