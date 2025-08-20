#!/usr/bin/env python3
"""
Test the Dynamic Agent Generator
"""

import asyncio
import sys
from pathlib import Path

# Add the agents directory to path
sys.path.append(str(Path(__file__).parent))

from mcp_services.meta.dynamic_agent_generator import DynamicAgentGenerator

async def main():
    generator = DynamicAgentGenerator()
    
    print("🤖 Dynamic Agent Generator Test\n")
    
    # 1. Identify missing services
    print("1. Identifying missing services...")
    missing = await generator.identify_missing_services("Fed Job Advisor")
    
    print(f"Found {len(missing)} missing service agents:")
    for service in missing:
        print(f"   - {service['service']} ({service['priority']} priority)")
    print()
    
    # 2. Generate all missing agents
    print("2. Generating missing agents...")
    results = await generator.bulk_generate_agents(missing)
    
    print(f"✅ Generated {len(results['generated'])} agents:")
    for result in results['generated']:
        print(f"   - {result['service_name']} → {result['agent_path']}")
        print(f"     Category: {result['category']}, Model: {result['model']}")
    
    if results['failed']:
        print(f"\n❌ Failed to generate {len(results['failed'])} agents:")
        for failure in results['failed']:
            print(f"   - {failure['service']}: {failure['error']}")
    
    print(f"\n📊 Summary: {len(results['generated'])}/{results['total']} agents generated successfully")

if __name__ == "__main__":
    asyncio.run(main())