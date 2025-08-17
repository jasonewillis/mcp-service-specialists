"""
LangGraph Integration Demonstration Examples
Practical examples showing how to use the Fed Job Advisor LangGraph orchestrator
with streaming, time travel debugging, and compliance enforcement.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.orchestrator.fed_job_orchestrator import get_orchestrator, WorkflowType
from app.orchestrator.debugging.time_travel import DebugLevel
from app.orchestrator.compliance.merit_hiring_gates import get_compliance_gates

# Configure logging for examples
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LangGraphDemo:
    """Demonstration class for LangGraph integration examples"""
    
    def __init__(self, enable_time_travel: bool = True, debug_level: DebugLevel = DebugLevel.DETAILED):
        """Initialize demo with orchestrator and compliance gates"""
        
        self.orchestrator = get_orchestrator(
            enable_time_travel=enable_time_travel,
            debug_level=debug_level
        )
        self.compliance_gates = get_compliance_gates(
            enable_streaming=True,
            enable_dynamic_interrupts=True
        )
        
        print(f"\n🚀 LangGraph Demo initialized")
        print(f"   Time Travel: {'✅ Enabled' if enable_time_travel else '❌ Disabled'}")
        print(f"   Debug Level: {debug_level.value}")
        print(f"   Streaming: ✅ Enabled")
        print(f"   Dynamic Interrupts: ✅ Enabled")
    
    def print_separator(self, title: str):
        """Print a visual separator for demo sections"""
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")
    
    def print_result_summary(self, result: Dict[str, Any], title: str = "Result"):
        """Print a formatted summary of the result"""
        print(f"\n📊 {title} Summary:")
        print(f"   Success: {'✅' if result.get('success', False) else '❌'}")
        print(f"   Session ID: {result.get('session_id', 'N/A')}")
        print(f"   Progress: {result.get('progress_percentage', 0):.1f}%")
        print(f"   Warnings: {len(result.get('warnings', []))}")
        print(f"   Compliance Violations: {len(result.get('compliance_violations', []))}")
        print(f"   Human Approvals Needed: {len(result.get('human_approvals_needed', []))}")
        print(f"   Streaming Events: {len(result.get('streaming_events', []))}")
        
        if result.get('debug_info'):
            debug_info = result['debug_info']
            print(f"   Debug Mode: {'✅' if debug_info.get('debug_mode') else '❌'}")
            if 'performance_metrics' in debug_info:
                metrics = debug_info['performance_metrics']
                if 'total_duration' in metrics:
                    print(f"   Total Duration: {metrics['total_duration']:.2f}s")
        
        if result.get('response'):
            response_preview = result['response'][:200] + "..." if len(result['response']) > 200 else result['response']
            print(f"   Response Preview: {response_preview}")
    
    def print_streaming_events(self, events: list, limit: int = 5):
        """Print recent streaming events"""
        if not events:
            return
        
        print(f"\n📡 Recent Streaming Events (last {limit}):")
        for event in events[-limit:]:
            timestamp = event.get('timestamp', 'N/A')[:19]  # Just date and time
            event_type = event.get('event_type', 'unknown')
            data = event.get('data', {})
            
            print(f"   [{timestamp}] {event_type}")
            if 'message' in data:
                print(f"      📝 {data['message']}")
            if 'progress' in data:
                print(f"      📊 Progress: {data['progress']:.1f}%")
    
    def print_compliance_violations(self, violations: list):
        """Print compliance violations in a readable format"""
        if not violations:
            print("   ✅ No compliance violations detected")
            return
        
        print(f"   ⚠️  {len(violations)} Compliance Violation(s):")
        for i, violation in enumerate(violations, 1):
            print(f"      {i}. Type: {violation.get('type', 'unknown')}")
            print(f"         Level: {violation.get('level', 'unknown')}")
            print(f"         Message: {violation.get('message', 'No message')}")
            if violation.get('action_blocked'):
                print(f"         🚫 Action Blocked: Yes")

    async def example_1_user_job_search(self):
        """Example 1: User searching for federal data scientist job"""
        
        self.print_separator("Example 1: Federal Data Scientist Job Search")
        
        print("\n🔍 Scenario: User looking for federal data scientist positions in Washington DC")
        print("   This example demonstrates the user-facing workflow with job matching and career guidance.")
        
        query = """I'm looking for federal data scientist positions in the Washington DC area. 
        I have a PhD in Statistics and 8 years of experience in machine learning. 
        I currently hold a Secret clearance. What opportunities are available and 
        what should I know about the application process?"""
        
        print(f"\n📝 User Query: {query[:100]}...")
        
        try:
            result = await self.orchestrator.process_request(
                user_id="demo_user_001",
                query=query,
                session_id="job_search_demo",
                context={
                    "location_preference": "Washington DC",
                    "education_level": "PhD",
                    "experience_years": 8,
                    "clearance_level": "Secret",
                    "skills": ["machine learning", "statistics", "python", "r"]
                },
                enable_streaming=True,
                debug_mode=True
            )
            
            self.print_result_summary(result, "Job Search")
            self.print_streaming_events(result.get('streaming_events', []))
            self.print_compliance_violations(result.get('compliance_violations', []))
            
            # Show recommendations if available
            if result.get('data') and 'recommendations' in result['data']:
                recommendations = result['data']['recommendations']
                print(f"\n💡 Job Recommendations ({len(recommendations)}):")
                for i, rec in enumerate(recommendations[:3], 1):  # Show first 3
                    print(f"   {i}. {rec}")
            
            return result
            
        except Exception as e:
            logger.error(f"Example 1 failed: {e}")
            print(f"❌ Error: {e}")
            return None
    
    async def example_2_platform_development(self):
        """Example 2: Platform development feature request"""
        
        self.print_separator("Example 2: Platform Development Feature Request")
        
        print("\n🔧 Scenario: Admin requesting new job recommendation algorithm")
        print("   This example demonstrates the platform development workflow with cost monitoring.")
        
        query = """Implement a new machine learning-based job recommendation algorithm 
        that analyzes user profiles and matches them with federal positions based on 
        skills, experience, and clearance requirements. Include A/B testing capabilities 
        and performance metrics tracking."""
        
        print(f"\n📝 Development Request: {query[:100]}...")
        
        try:
            result = await self.orchestrator.process_request(
                user_id="admin_user_001",
                query=query,
                session_id="platform_dev_demo",
                context={
                    "project_type": "enhancement", 
                    "priority": "high",
                    "deadline": "2024-04-01",
                    "budget_limit": 0,  # $0 external development constraint
                    "team_size": 1,     # Solo developer
                    "estimated_hours": 120
                },
                enable_streaming=True,
                debug_mode=True
            )
            
            self.print_result_summary(result, "Platform Development")
            self.print_streaming_events(result.get('streaming_events', []))
            self.print_compliance_violations(result.get('compliance_violations', []))
            
            # Show development phases if available
            if result.get('data') and 'completed_phases' in result['data']:
                phases = result['data']['completed_phases']
                print(f"\n🏗️ Development Phases Completed ({len(phases)}):")
                for phase in phases:
                    print(f"   ✅ {phase}")
            
            # Show cost analysis if available
            if result.get('data') and 'cost_analysis' in result['data']:
                cost_analysis = result['data']['cost_analysis']
                print(f"\n💰 Cost Analysis:")
                print(f"   Estimated Hours: {cost_analysis.get('estimated_hours', 'N/A')}")
                print(f"   Budget Used: ${cost_analysis.get('budget_used', 0)}")
                print(f"   Budget Exceeded: {'⚠️ Yes' if cost_analysis.get('budget_exceeded') else '✅ No'}")
            
            return result
            
        except Exception as e:
            logger.error(f"Example 2 failed: {e}")
            print(f"❌ Error: {e}")
            return None
    
    async def example_3_compliance_violation_handling(self):
        """Example 3: Compliance violation detection and handling"""
        
        self.print_separator("Example 3: Compliance Violation Detection")
        
        print("\n🚨 Scenario: User requesting essay content generation (should be blocked)")
        print("   This example demonstrates compliance enforcement and dynamic interrupts.")
        
        # This query should trigger multiple compliance violations
        query = """Write my federal job essay about my data science experience. 
        Don't worry about the 200-word limit - make it as long as needed. 
        I need you to create the complete narrative response for my application."""
        
        print(f"\n📝 Problematic Query: {query[:100]}...")
        print("   ⚠️  Expected violations: Essay content generation, word limit guidance")
        
        try:
            result = await self.orchestrator.process_request(
                user_id="demo_user_002", 
                query=query,
                session_id="compliance_demo",
                context={
                    "request_type": "essay_help",
                    "application_stage": "drafting"
                },
                enable_streaming=True,
                debug_mode=True
            )
            
            self.print_result_summary(result, "Compliance Check")
            self.print_streaming_events(result.get('streaming_events', []))
            self.print_compliance_violations(result.get('compliance_violations', []))
            
            # Show dynamic interrupts if triggered
            if result.get('dynamic_interrupts'):
                print(f"\n🛑 Dynamic Interrupts Triggered ({len(result['dynamic_interrupts'])}):")
                for interrupt in result['dynamic_interrupts']:
                    print(f"   ⚡ {interrupt}")
            
            # Show human approvals needed
            if result.get('human_approvals_needed'):
                print(f"\n👤 Human Approvals Required ({len(result['human_approvals_needed'])}):")
                for approval in result['human_approvals_needed']:
                    print(f"   🔍 {approval}")
            
            return result
            
        except Exception as e:
            logger.error(f"Example 3 failed: {e}")
            print(f"❌ Error: {e}")
            return None
    
    async def example_4_checkpoint_recovery_demo(self):
        """Example 4: Checkpoint recovery demonstration"""
        
        self.print_separator("Example 4: Checkpoint Recovery and Time Travel")
        
        if not self.orchestrator.time_travel_enabled:
            print("   ⚠️  Time travel debugging not enabled - skipping checkpoint demo")
            return None
        
        print("\n⏰ Scenario: Process request with checkpoints, then demonstrate recovery")
        print("   This example shows time travel debugging and checkpoint recovery capabilities.")
        
        query = """Analyze the federal job market trends for cybersecurity positions 
        over the past 5 years. Include salary trends, agency preferences, and 
        required qualifications evolution."""
        
        print(f"\n📝 Analysis Query: {query[:100]}...")
        
        try:
            # Process initial request with checkpoints
            result = await self.orchestrator.process_request(
                user_id="demo_user_003",
                query=query,
                session_id="checkpoint_demo",
                context={"analysis_type": "market_trends", "time_period": "5_years"},
                enable_streaming=True,
                debug_mode=True
            )
            
            self.print_result_summary(result, "Initial Processing")
            
            if result.get('debug_info', {}).get('checkpoint_id'):
                checkpoint_id = result['debug_info']['checkpoint_id']
                session_id = result.get('session_id')
                
                print(f"\n🎯 Checkpoint Created: {checkpoint_id}")
                print("   Demonstrating checkpoint recovery...")
                
                # Demonstrate replay from checkpoint
                replay_result = await self.orchestrator.replay_from_checkpoint(
                    session_id=session_id,
                    checkpoint_id=checkpoint_id
                )
                
                if replay_result.get('success'):
                    print(f"   ✅ Checkpoint replay successful")
                    print(f"   🔄 Replay data available: {bool(replay_result.get('replay_data'))}")
                else:
                    print(f"   ❌ Checkpoint replay failed: {replay_result.get('error', 'Unknown error')}")
                
            else:
                print("   ⚠️  No checkpoint created in this session")
            
            return result
            
        except Exception as e:
            logger.error(f"Example 4 failed: {e}")
            print(f"❌ Error: {e}")
            return None
    
    async def example_5_real_time_streaming_progress(self):
        """Example 5: Real-time streaming progress demonstration"""
        
        self.print_separator("Example 5: Real-time Streaming Progress")
        
        print("\n📡 Scenario: Complex multi-step analysis with real-time progress updates")
        print("   This example demonstrates streaming events and real-time monitoring.")
        
        query = """Provide a comprehensive analysis of federal data positions including:
        1. Current job openings analysis
        2. Salary and benefits comparison
        3. Career progression opportunities  
        4. Skills gap analysis
        5. Recommendations for career development"""
        
        print(f"\n📝 Complex Query: {query[:100]}...")
        print("   📊 Monitoring real-time progress...")
        
        try:
            # Start the request
            session_id = f"streaming_demo_{datetime.now().timestamp()}"
            
            # Process with streaming enabled
            result = await self.orchestrator.process_request(
                user_id="demo_user_004",
                query=query,
                session_id=session_id,
                context={"analysis_depth": "comprehensive"},
                enable_streaming=True,
                debug_mode=False  # Disable debug for performance
            )
            
            self.print_result_summary(result, "Streaming Analysis")
            
            # Demonstrate real-time status monitoring
            try:
                status = await self.orchestrator.get_real_time_status(session_id)
                print(f"\n📊 Real-time Status:")
                print(f"   Current Step: {status.get('current_step', 'N/A')}")
                print(f"   Progress: {status.get('progress_percentage', 0):.1f}%")
                print(f"   Completed Steps: {len(status.get('completed_steps', []))}")
                print(f"   Active Agents: {status.get('active_agents', 0)}")
                print(f"   Warnings: {status.get('warnings_count', 0)}")
                
            except Exception as status_error:
                print(f"   ⚠️  Could not retrieve real-time status: {status_error}")
            
            # Show detailed streaming events
            streaming_events = result.get('streaming_events', [])
            if streaming_events:
                self.print_streaming_events(streaming_events, limit=10)
                
                # Analyze event types
                event_types = {}
                for event in streaming_events:
                    event_type = event.get('event_type', 'unknown')
                    event_types[event_type] = event_types.get(event_type, 0) + 1
                
                print(f"\n📈 Event Type Summary:")
                for event_type, count in sorted(event_types.items()):
                    print(f"   {event_type}: {count} events")
            
            return result
            
        except Exception as e:
            logger.error(f"Example 5 failed: {e}")
            print(f"❌ Error: {e}")
            return None
    
    async def bonus_example_session_history(self):
        """Bonus: Demonstrate session history and conversation continuity"""
        
        self.print_separator("Bonus Example: Session History and Continuity")
        
        print("\n💬 Scenario: Multi-turn conversation with session persistence")
        print("   This example shows conversation history and context continuity.")
        
        session_id = f"conversation_demo_{datetime.now().timestamp()}"
        
        # First query
        query1 = "What are the basic requirements for GS-13 data scientist positions?"
        print(f"\n📝 Query 1: {query1}")
        
        try:
            result1 = await self.orchestrator.process_request(
                user_id="demo_user_005",
                query=query1,
                session_id=session_id,
                enable_streaming=False  # Disable for cleaner output
            )
            
            print(f"   ✅ Response 1: {result1.get('response', 'No response')[:100]}...")
            
            # Second query building on first
            query2 = "What about GS-14 level? How much more experience is needed?"
            print(f"\n📝 Query 2: {query2}")
            
            result2 = await self.orchestrator.process_request(
                user_id="demo_user_005",
                query=query2,
                session_id=session_id,
                enable_streaming=False
            )
            
            print(f"   ✅ Response 2: {result2.get('response', 'No response')[:100]}...")
            
            # Get session history
            history = await self.orchestrator.get_session_history(
                session_id=session_id,
                include_streaming_events=True
            )
            
            print(f"\n📚 Session History Summary:")
            print(f"   Session ID: {history.get('session_id', 'N/A')}")
            print(f"   Conversation Turns: {len(history.get('conversation_history', []))}")
            print(f"   Current Progress: {history.get('current_progress', 0):.1f}%")
            print(f"   Current Step: {history.get('current_step', 'N/A')}")
            print(f"   Warnings: {len(history.get('warnings', []))}")
            
            # Show conversation flow
            if history.get('conversation_history'):
                print(f"\n💬 Conversation Flow:")
                for i, msg in enumerate(history['conversation_history']):
                    msg_type = "👤 User" if msg.get('type') == 'human' else "🤖 Assistant"
                    content_preview = msg.get('content', '')[:80] + "..." if len(msg.get('content', '')) > 80 else msg.get('content', '')
                    print(f"   {i+1}. {msg_type}: {content_preview}")
            
            return {"result1": result1, "result2": result2, "history": history}
            
        except Exception as e:
            logger.error(f"Bonus example failed: {e}")
            print(f"❌ Error: {e}")
            return None
    
    async def run_all_examples(self):
        """Run all demo examples in sequence"""
        
        print("\n🎬 Running All LangGraph Integration Examples")
        print("   This comprehensive demo covers all major features of the system.")
        
        results = {}
        
        # Run each example
        examples = [
            ("User Job Search", self.example_1_user_job_search),
            ("Platform Development", self.example_2_platform_development), 
            ("Compliance Violation", self.example_3_compliance_violation_handling),
            ("Checkpoint Recovery", self.example_4_checkpoint_recovery_demo),
            ("Streaming Progress", self.example_5_real_time_streaming_progress),
            ("Session History", self.bonus_example_session_history)
        ]
        
        for example_name, example_func in examples:
            try:
                print(f"\n⏳ Running {example_name} example...")
                result = await example_func()
                results[example_name] = result
                
                if result:
                    print(f"   ✅ {example_name} completed successfully")
                else:
                    print(f"   ⚠️  {example_name} completed with issues")
                    
            except Exception as e:
                logger.error(f"{example_name} example failed: {e}")
                print(f"   ❌ {example_name} failed: {e}")
                results[example_name] = None
        
        # Final summary
        self.print_separator("Demo Complete - Final Summary")
        
        successful = len([r for r in results.values() if r is not None])
        total = len(results)
        
        print(f"\n📊 Demo Results:")
        print(f"   Total Examples: {total}")
        print(f"   Successful: {successful}")
        print(f"   Success Rate: {successful/total*100:.1f}%")
        
        for example_name, result in results.items():
            status = "✅ Success" if result else "❌ Failed"
            print(f"   {status}: {example_name}")
        
        return results


async def main():
    """Main demo execution function"""
    
    print("🎯 Fed Job Advisor LangGraph Integration Demo")
    print("   Demonstrating comprehensive orchestrator capabilities")
    
    # Check command line arguments for specific examples
    import sys
    
    if len(sys.argv) > 1:
        example_num = sys.argv[1]
        demo = LangGraphDemo()
        
        if example_num == "1":
            await demo.example_1_user_job_search()
        elif example_num == "2":
            await demo.example_2_platform_development()
        elif example_num == "3":
            await demo.example_3_compliance_violation_handling()
        elif example_num == "4":
            await demo.example_4_checkpoint_recovery_demo()
        elif example_num == "5":
            await demo.example_5_real_time_streaming_progress()
        elif example_num == "bonus":
            await demo.bonus_example_session_history()
        elif example_num == "all":
            await demo.run_all_examples()
        else:
            print(f"❌ Unknown example: {example_num}")
            print("   Available examples: 1, 2, 3, 4, 5, bonus, all")
    else:
        # Run interactive demo
        demo = LangGraphDemo()
        
        print("\n🎮 Interactive Demo Mode")
        print("   Choose an example to run:")
        print("   1. User Job Search (user-facing workflow)")
        print("   2. Platform Development (development workflow)")
        print("   3. Compliance Violation (compliance enforcement)")
        print("   4. Checkpoint Recovery (time travel debugging)")
        print("   5. Streaming Progress (real-time monitoring)")
        print("   6. Session History (conversation continuity)")
        print("   7. Run All Examples")
        print("   0. Exit")
        
        while True:
            try:
                choice = input("\n🤔 Select example (0-7): ").strip()
                
                if choice == "0":
                    print("👋 Goodbye!")
                    break
                elif choice == "1":
                    await demo.example_1_user_job_search()
                elif choice == "2":
                    await demo.example_2_platform_development()
                elif choice == "3":
                    await demo.example_3_compliance_violation_handling()
                elif choice == "4":
                    await demo.example_4_checkpoint_recovery_demo()
                elif choice == "5":
                    await demo.example_5_real_time_streaming_progress()
                elif choice == "6":
                    await demo.bonus_example_session_history()
                elif choice == "7":
                    await demo.run_all_examples()
                else:
                    print("❌ Invalid choice. Please select 0-7.")
                
                # Ask if user wants to continue
                continue_choice = input("\n🔄 Run another example? (y/n): ").strip().lower()
                if continue_choice != 'y':
                    print("👋 Demo complete!")
                    break
                    
            except KeyboardInterrupt:
                print("\n\n👋 Demo interrupted. Goodbye!")
                break
            except Exception as e:
                logger.error(f"Demo error: {e}")
                print(f"❌ Error: {e}")


if __name__ == "__main__":
    # Run the demo
    asyncio.run(main())