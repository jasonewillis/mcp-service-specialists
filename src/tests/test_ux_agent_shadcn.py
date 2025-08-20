#!/usr/bin/env python3
"""
Test UX/Design Agent with shadcn/ui Components
Demonstrates creating modern UI components for Fed Job Advisor
"""

import requests
import json
import time

API_URL = "http://localhost:8003"

def test_ux_agent(task):
    """Test the UX agent with a design task"""
    print(f"\n{'='*80}")
    print("🎨 UX/DESIGN AGENT - shadcn/ui Component Generation")
    print(f"{'='*80}")
    print(f"\nTask: {task}\n")
    
    # Since we don't have a dedicated UX endpoint yet, we'll simulate it
    # In production, this would call the actual UX agent
    
    # For now, let's use the frontend agent as a proxy
    try:
        response = requests.post(
            f"{API_URL}/test/frontend",
            params={"task": task},
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Component Generated Successfully!")
            print("\n📝 Generated Code:")
            print("-" * 40)
            print(result['response'][:2000])  # First 2000 chars
            if len(result['response']) > 2000:
                print("\n[... additional code truncated ...]")
            return result
        else:
            print(f"❌ Error: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return None

def main():
    print("🚀 SHADCN/UI COMPONENT GENERATION TEST")
    print("=" * 80)
    print("Testing UX/Design Agent with modern React component library")
    print("Using shadcn/ui for beautiful, accessible components")
    
    # Test 1: Create a Job Search Filter Component
    print("\n" + "="*80)
    print("TEST 1: Job Search Filter Component")
    print("="*80)
    
    task1 = """Create a job search filter component using shadcn/ui components with:
    - Grade level selector (GS-5 through GS-15)
    - Location dropdown
    - Job series input
    - Salary range slider
    - Clear filters button
    
    Use shadcn/ui components like Select, Input, Slider, and Button.
    Include Tailwind CSS for styling and make it fully accessible."""
    
    test_ux_agent(task1)
    
    # Test 2: Create a Resume Upload Component
    print("\n" + "="*80)
    print("TEST 2: Resume Upload Component")
    print("="*80)
    
    task2 = """Create a resume upload component using shadcn/ui with:
    - Drag and drop area
    - File type validation (PDF, DOCX)
    - Upload progress indicator
    - Success/error messages using Toast
    - Preview of uploaded file
    
    Use shadcn/ui Card, Button, Progress, and Toast components.
    Make it responsive and accessible."""
    
    test_ux_agent(task2)
    
    # Test 3: Create a Job Application Status Dashboard
    print("\n" + "="*80)
    print("TEST 3: Application Status Dashboard")
    print("="*80)
    
    task3 = """Create an application status dashboard using shadcn/ui with:
    - Status cards showing application stages
    - Progress indicators
    - Timeline component
    - Action buttons for each application
    
    Use shadcn/ui Card, Badge, Progress, and Tabs components.
    Include icons from lucide-react and make it mobile-responsive."""
    
    test_ux_agent(task3)
    
    # Summary
    print("\n" + "="*80)
    print("📊 COMPONENT GENERATION SUMMARY")
    print("="*80)
    
    print("""
✨ Key Benefits of shadcn/ui for Fed Job Advisor:

1. **Accessibility First**: All components follow WCAG 2.1 guidelines
2. **Federal Compliance**: Clean, professional design suitable for government
3. **Customizable**: Easy to match federal design standards
4. **Performance**: Lightweight, no unnecessary dependencies
5. **TypeScript**: Full type safety for reliability

🎯 Recommended Components for Fed Job Advisor:
- Card: Job listings, user profiles
- Form: Application forms, profile editing
- Table: Job comparison, application tracking
- Dialog: Confirmations, detailed views
- Toast: Notifications, status updates
- Tabs: Dashboard sections, navigation

💡 Next Steps:
1. Install shadcn/ui in Fed Job Advisor frontend
2. Replace existing components with shadcn/ui versions
3. Create consistent design system
4. Add dark mode support
5. Ensure Section 508 compliance
""")

if __name__ == "__main__":
    main()