#!/usr/bin/env python3
"""
Sentry Documentation Scraper for Fed Job Advisor
Focuses on essential error monitoring capabilities for production deployment
Uses the webscraping MCP agent to scrape Sentry documentation
"""

import asyncio
import json
import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Import our webscraping specialist
from mcp_services.external.webscraping_specialist import WebscrapingSpecialist

class SentryDocumentationScraper:
    """Orchestrates the scraping of Sentry documentation for Fed Job Advisor needs"""
    
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.scraper = WebscrapingSpecialist()
        
        # Configure scraping for respectful access to Sentry docs
        self.scraper.delay_between_requests = 2.0  # 2 seconds between requests
        self.scraper.max_concurrent = 2  # Conservative concurrent limit
        self.scraper.timeout = 45  # Longer timeout for large pages
        
        # Define scraping sections focused on Fed Job Advisor needs
        self.scraping_sections = {
            "01_platform_setup": {
                "description": "Platform setup and configuration for Python/JavaScript",
                "sections": {
                    "python_setup": {
                        "url": "https://docs.sentry.io/platforms/python/",
                        "patterns": [
                            r"/platforms/python/",
                            r"/platforms/python/configuration/",
                            r"/platforms/python/fastapi/"
                        ],
                        "max_pages": 15
                    },
                    "javascript_setup": {
                        "url": "https://docs.sentry.io/platforms/javascript/",
                        "patterns": [
                            r"/platforms/javascript/",
                            r"/platforms/javascript/guides/nextjs/",
                            r"/platforms/javascript/guides/react/"
                        ],
                        "max_pages": 12
                    }
                }
            },
            "02_error_monitoring": {
                "description": "Error tracking and performance monitoring essentials",
                "sections": {
                    "error_tracking": {
                        "url": "https://docs.sentry.io/product/issues/",
                        "patterns": [
                            r"/product/issues/",
                            r"/product/alerts/",
                            r"/concepts/key-terms/"
                        ],
                        "max_pages": 10
                    },
                    "performance_monitoring": {
                        "url": "https://docs.sentry.io/product/performance/",
                        "patterns": [
                            r"/product/performance/",
                            r"/product/performance/getting-started/",
                            r"/platforms/python/performance/"
                        ],
                        "max_pages": 8
                    }
                }
            },
            "03_integration": {
                "description": "Integration patterns for production deployment",
                "sections": {
                    "production_config": {
                        "url": "https://docs.sentry.io/product/accounts/getting-started/",
                        "patterns": [
                            r"/product/accounts/",
                            r"/concepts/environments/",
                            r"/product/releases/"
                        ],
                        "max_pages": 8
                    },
                    "api_integration": {
                        "url": "https://docs.sentry.io/api/",
                        "patterns": [
                            r"/api/",
                            r"/api/events/",
                            r"/api/releases/"
                        ],
                        "max_pages": 10
                    }
                }
            }
        }
        
        self.total_scraped = 0
        self.section_results = {}
    
    def clean_filename(self, text: str) -> str:
        """Create a clean filename from text"""
        # Remove or replace problematic characters
        clean = re.sub(r'[^\w\s-]', '', text.strip())
        clean = re.sub(r'[-\s]+', '_', clean)
        return clean.lower()[:100]  # Limit length
    
    def extract_title_from_url(self, url: str) -> str:
        """Extract a meaningful title from URL"""
        # Remove domain and clean up
        url_clean = url.replace('https://docs.sentry.io/', '')
        url_clean = url_clean.replace('/', '_').replace('#', '_').replace('?', '_')
        return url_clean or 'index'
    
    def filter_production_content(self, content: str) -> str:
        """Filter content to focus on production-ready features"""
        # Keywords that indicate development/testing content to de-emphasize
        dev_keywords = [
            'debug mode',
            'development server',
            'localhost',
            'example.com',
            'test data',
            'sample project'
        ]
        
        # Simple filtering - in production would be more sophisticated
        lines = content.split('\n')
        filtered_lines = []
        
        for line in lines:
            line_lower = line.lower()
            # Keep all lines but add production context markers
            if any(keyword in line_lower for keyword in dev_keywords):
                if not line.startswith('#'):  # Don't modify headers
                    line = f"<!-- DEV: {line} -->"
            filtered_lines.append(line)
        
        return '\n'.join(filtered_lines)
    
    def convert_to_markdown(self, content: str, metadata: Dict[str, Any], url: str) -> str:
        """Convert scraped content to markdown with frontmatter"""
        
        # Filter for production focus
        filtered_content = self.filter_production_content(content)
        
        # Create YAML frontmatter
        title = metadata.get('title', 'Sentry Documentation').replace('"', '\\"')
        description = metadata.get('description', '').replace('"', '\\"')
        keywords = metadata.get('keywords', '').replace('"', '\\"')
        
        frontmatter = [
            "---",
            f'title: "{title}"',
            f'source_url: "{url}"',
            f'scraped_date: "{datetime.now().isoformat()}"',
            f'description: "{description}"',
            'platform: "sentry"',
            'category: "error_monitoring"',
            'stack: "fed_job_advisor"'
        ]
        
        if keywords:
            frontmatter.append(f'keywords: "{keywords}"')
        
        # Add Fed Job Advisor context
        frontmatter.append('note: "Documentation focused on Fed Job Advisor production deployment"')
        
        frontmatter.append("---")
        frontmatter.append("")
        
        # Add title if not in content
        if metadata.get('title') and metadata['title'] not in filtered_content[:200]:
            filtered_content = f"# {metadata['title']}\n\n{filtered_content}"
        
        # Add production deployment context
        filtered_content = f"**Note: This documentation is focused on production deployment for Fed Job Advisor**\n\n{filtered_content}"
        
        return '\n'.join(frontmatter) + filtered_content
    
    async def scrape_section(self, category: str, section_name: str, section_config: Dict[str, Any]) -> Dict[str, Any]:
        """Scrape a specific documentation section"""
        
        print(f"🔍 Scraping {category}/{section_name}: {section_config['url']}")
        
        try:
            result = await self.scraper.traverse_documentation(
                start_url=section_config['url'],
                max_depth=2,  # Moderate depth for Sentry docs
                max_pages=section_config['max_pages'],
                link_patterns=section_config['patterns']
            )
            
            if result['success']:
                total_pages = result['total_pages']
                print(f"✅ Successfully scraped {total_pages} pages from {section_name}")
                
                # Create directory for this section
                section_dir = self.output_dir / category / section_name
                section_dir.mkdir(parents=True, exist_ok=True)
                
                # Save each scraped page
                saved_files = []
                for url, page_data in result['content'].items():
                    if page_data['success']:
                        # Generate filename
                        url_title = self.extract_title_from_url(url)
                        page_title = self.clean_filename(page_data.get('title', ''))
                        filename = f"{url_title}_{page_title}.md" if page_title else f"{url_title}.md"
                        filename = filename.replace('__', '_')
                        
                        # Convert to markdown
                        markdown_content = self.convert_to_markdown(
                            page_data['content'], 
                            page_data['metadata'], 
                            url
                        )
                        
                        # Save file
                        file_path = section_dir / filename
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(markdown_content)
                        
                        saved_files.append(str(file_path))
                
                # Save section metadata
                section_metadata = {
                    "section": section_name,
                    "category": category,
                    "scraped_date": datetime.now().isoformat(),
                    "source_url": section_config['url'],
                    "total_pages": total_pages,
                    "saved_files": saved_files,
                    "scraping_config": section_config,
                    "platform": "sentry",
                    "purpose": "Fed Job Advisor error monitoring and performance tracking"
                }
                
                metadata_path = section_dir / "_section_metadata.json"
                with open(metadata_path, 'w') as f:
                    json.dump(section_metadata, f, indent=2)
                
                print(f"💾 Saved {len(saved_files)} files to {section_dir}")
                self.total_scraped += total_pages
                
                return {
                    "success": True,
                    "pages_scraped": total_pages,
                    "files_saved": len(saved_files),
                    "directory": str(section_dir)
                }
                
            else:
                print(f"❌ Failed to scrape {section_name}: {result.get('error')}")
                return {"success": False, "error": result.get('error')}
                
        except Exception as e:
            print(f"❌ Exception scraping {section_name}: {e}")
            return {"success": False, "error": str(e)}
    
    async def scrape_all_sections(self):
        """Scrape all defined Sentry documentation sections"""
        
        print("🚀 Starting Sentry documentation scraping for Fed Job Advisor")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"⚙️  Scraping configuration: {self.scraper.delay_between_requests}s delay, max {self.scraper.max_concurrent} concurrent")
        print("💡 Focus: Production error monitoring and performance tracking")
        print("=" * 70)
        
        start_time = datetime.now()
        
        for category, category_config in self.scraping_sections.items():
            print(f"\n📂 Category: {category} - {category_config['description']}")
            print("-" * 50)
            
            category_results = {}
            
            for section_name, section_config in category_config['sections'].items():
                result = await self.scrape_section(category, section_name, section_config)
                category_results[section_name] = result
                
                # Add delay between sections to be respectful
                await asyncio.sleep(3)
            
            self.section_results[category] = category_results
        
        # Generate final summary
        end_time = datetime.now()
        duration = end_time - start_time
        
        summary = {
            "scraping_session": {
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(), 
                "duration_seconds": duration.total_seconds(),
                "total_pages_scraped": self.total_scraped,
                "focus": "Fed Job Advisor error monitoring and performance tracking",
                "platform": "sentry"
            },
            "results_by_category": self.section_results,
            "output_directory": str(self.output_dir),
            "features_covered": [
                "Python/FastAPI Integration",
                "JavaScript/Next.js Integration", 
                "Error Tracking and Alerts",
                "Performance Monitoring",
                "Production Configuration",
                "API Integration"
            ]
        }
        
        # Save summary
        summary_path = self.output_dir / "scraping_summary.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print("\n" + "=" * 70)
        print("🎉 Sentry Documentation Scraping Complete!")
        print(f"📊 Total pages scraped: {self.total_scraped}")
        print(f"⏱️  Total time: {duration}")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"📋 Summary saved to: {summary_path}")
        print("💡 Coverage: Production-ready error monitoring for Fed Job Advisor")
        
        return summary

async def main():
    """Main scraping orchestration"""
    
    output_dir = "/Users/jasonewillis/Developer/jwRepos/JLWAI/Agents/docs/external_services/platforms/sentry/"
    
    scraper = SentryDocumentationScraper(output_dir)
    summary = await scraper.scrape_all_sections()
    
    return summary

if __name__ == "__main__":
    summary = asyncio.run(main())
    print(f"\n🏁 Sentry documentation scraping completed successfully!")
    print(f"📈 Final statistics: {summary['scraping_session']['total_pages_scraped']} pages scraped")