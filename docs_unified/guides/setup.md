# Fed Job Advisor MCP Server Setup

## ✅ **MCP Server Successfully Created**

Your Fed Job Advisor agents are now available as an MCP server that integrates directly with Claude Code!

## **Available Agent Tools** (10 total)

### **Role-Based Analysis**
- `analyze_data_scientist_profile` - Series 1560 specialist
- `analyze_statistician_profile` - Series 1530 specialist  
- `analyze_database_admin_profile` - Series 2210/0334 specialist
- `analyze_devops_profile` - DevOps engineer specialist
- `analyze_it_specialist_profile` - General IT specialist

### **Compliance & Optimization**
- `check_essay_compliance` - Merit Hiring essay analysis (never writes)
- `analyze_resume_compression` - 2-page federal resume optimization
- `research_executive_orders` - Policy research and analysis

### **Analytics & Intelligence**
- `analyze_job_market` - Market trends and intelligence
- `orchestrate_job_collection` - Pipeline monitoring

## **Setup Instructions**

### **1. Add MCP Server to Claude Code**

Add this to your Claude Code MCP configuration:

```json
{
  "mcpServers": {
    "fed-job-advisor": {
      "command": "python",
      "args": ["/Users/jasonewillis/Developer/jwRepos/JLWAI/Agents/mcp_server.py"],
      "env": {},
      "disabled": false
    }
  }
}
```

**Location of MCP config:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

### **2. Start Agent Service**

Before using MCP tools, start the agent service:

```bash
cd /Users/jasonewillis/Developer/jwRepos/JLWAI/Agents
python main.py
```

The agent service will run on `http://localhost:8001`

### **3. Restart Claude Code**

After adding the MCP configuration, restart Claude Code to load the new server.

### **4. Verify Integration**

In Claude Code, the tools will be available automatically. You can verify by asking:

"What agent tools are available?"

You should see all 10 Fed Job Advisor tools listed.

## **Usage Examples**

### **Analyze a Data Scientist Profile**
```
Analyze this candidate for a federal data scientist position:

Skills: Python, R, TensorFlow, AWS, SQL
Experience: 5 years in machine learning, worked on fraud detection...
Target Grade: GS-13
```

Claude Code will automatically use `analyze_data_scientist_profile` tool.

### **Check Essay Compliance**
```
Check this federal essay for Merit Hiring compliance:

Essay: "During my time as a data analyst..."
Essay Number: 2
```

Claude Code will use `check_essay_compliance` tool.

### **Market Analysis**
```
What's the current job market like for GS-13 statistician positions?
```

Claude Code will use `analyze_job_market` tool.

## **Benefits**

✅ **Native Integration** - Tools appear as Claude Code capabilities
✅ **Automatic Orchestration** - Claude Code chains tools intelligently  
✅ **Context Awareness** - Tools access project context
✅ **No Manual API Calls** - Seamless workflow integration
✅ **Federal Expertise** - Specialized knowledge built-in

## **Troubleshooting**

### **"Agent service not running" error**
```bash
cd /Users/jasonewillis/Developer/jwRepos/JLWAI/Agents
python main.py
```

### **Tools not appearing in Claude Code**
1. Verify MCP config is correct
2. Restart Claude Code completely
3. Check agent service is running on port 8001

### **Test MCP Server**
```bash
cd /Users/jasonewillis/Developer/jwRepos/JLWAI/Agents
python test_mcp.py
```

## **Next Steps**

1. **Start agent service** (port 8001)
2. **Add MCP config** to Claude Code
3. **Restart Claude Code**
4. **Start using agents** for fedJobAdvisor development!

The MCP integration makes your specialized federal job agents available as native Claude Code tools, creating a powerful workflow for federal job application assistance.