#!/usr/bin/env python3
"""
Basic webscraping examples using the WebscrapingSpecialist
"""

import asyncio
import json
from mcp_services.external.webscraping_specialist import WebscrapingSpecialist

async def example_single_page_scrape():
    """Example: Scrape a single documentation page"""
    
    scraper = WebscrapingSpecialist()
    
    # Scrape Python documentation homepage
    result = await scraper.scrape_single_page(
        url="https://docs.python.org/3/",
        extract_links=True,
        content_selector="main"  # Target main content area
    )
    
    if result["success"]:
        print(f"✅ Successfully scraped: {result['title']}")
        print(f"📄 Content length: {len(result['content'])} characters")
        print(f"🔗 Found {len(result['links'])} links")
        print(f"📊 Metadata: {json.dumps(result['metadata'], indent=2)}")
        
        # Show first 200 characters of content
        print(f"📝 Content preview: {result['content'][:200]}...")
        
        # Show first 5 links
        print(f"🔗 Link examples:")
        for link in result['links'][:5]:
            print(f"   - {link}")
    else:
        print(f"❌ Scraping failed: {result['error']}")

async def example_documentation_traversal():
    """Example: Traverse a documentation site"""
    
    scraper = WebscrapingSpecialist()
    
    # Traverse FastAPI documentation (limited scope)
    result = await scraper.traverse_documentation(
        start_url="https://fastapi.tiangolo.com/",
        max_depth=2,           # Only go 2 levels deep
        max_pages=10,          # Limit to 10 pages for this example
        link_patterns=[        # Only follow tutorial and guide links
            r"/tutorial/",
            r"/guide/",
            r"/getting-started/"
        ]
    )
    
    if result["success"]:
        print(f"✅ Successfully traversed documentation")
        print(f"📚 Total pages scraped: {result['total_pages']}")
        print(f"🏁 Starting URL: {result['start_url']}")
        print(f"⚙️ Configuration: {json.dumps(result['configuration'], indent=2)}")
        
        # Show all scraped URLs
        print(f"📄 Scraped pages:")
        for url, page_data in result['content'].items():
            print(f"   - {page_data['title']} ({url})")
        
        # Show any errors encountered
        if result['errors']:
            print(f"⚠️ Errors encountered: {len(result['errors'])}")
            for error in result['errors']:
                print(f"   - {error['url']}: {error['error']}")
    else:
        print(f"❌ Traversal failed: {result['error']}")

async def example_custom_content_extraction():
    """Example: Custom content extraction with specific selectors"""
    
    scraper = WebscrapingSpecialist()
    
    # Scrape GitHub README with custom selector
    result = await scraper.scrape_single_page(
        url="https://github.com/python/cpython",
        extract_links=False,  # Don't need links for this example
        content_selector="article.markdown-body"  # GitHub README selector
    )
    
    if result["success"]:
        print(f"✅ Custom extraction successful")
        print(f"📄 Title: {result['title']}")
        print(f"📊 Headings found: {len(result['metadata']['headings'])}")
        
        # Show heading structure
        print(f"📋 Document structure:")
        for heading in result['metadata']['headings'][:10]:  # First 10 headings
            indent = "  " * (heading['level'] - 1)
            print(f"{indent}H{heading['level']}: {heading['text']}")
        
        # Show content preview
        print(f"📝 Content preview: {result['content'][:300]}...")
    else:
        print(f"❌ Custom extraction failed: {result['error']}")

async def main():
    """Run all examples"""
    
    print("🕷️ Webscraping Specialist Examples")
    print("=" * 50)
    
    print("\n1️⃣ Single Page Scraping Example")
    print("-" * 30)
    await example_single_page_scrape()
    
    print("\n2️⃣ Documentation Traversal Example")  
    print("-" * 30)
    await example_documentation_traversal()
    
    print("\n3️⃣ Custom Content Extraction Example")
    print("-" * 30)
    await example_custom_content_extraction()
    
    print("\n✅ All examples completed!")

if __name__ == "__main__":
    # Run the examples
    asyncio.run(main())