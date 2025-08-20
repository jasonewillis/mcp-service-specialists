#!/usr/bin/env python3
"""
Docker Documentation Scraper for Fed Job Advisor
Uses the webscraping MCP agent to systematically scrape Docker documentation
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

class DockerDocumentationScraper:
    """Orchestrates the scraping of Docker documentation using MCP webscraping agent"""
    
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.scraper = WebscrapingSpecialist()
        
        # Configure scraping for respectful access to Docker docs
        self.scraper.delay_between_requests = 2.0  # 2 seconds between requests
        self.scraper.max_concurrent = 2  # Conservative concurrent limit
        self.scraper.timeout = 45  # Longer timeout for large pages
        
        # Define scraping sections based on MCP agent research
        self.scraping_sections = {
            "01_essential": {
                "description": "Core deployment documentation",
                "sections": {
                    "compose": {
                        "url": "https://docs.docker.com/compose/",
                        "patterns": [r"/compose/", r"/guides/.*compose"],
                        "max_pages": 30
                    },
                    "engine": {
                        "url": "https://docs.docker.com/engine/",
                        "patterns": [r"/engine/", r"/guides/.*engine"],
                        "max_pages": 25
                    },
                    "build": {
                        "url": "https://docs.docker.com/build/",
                        "patterns": [r"/build/", r"/guides/.*build"],
                        "max_pages": 25
                    },
                    "deployment": {
                        "url": "https://docs.docker.com/guides/deployment/",
                        "patterns": [r"/guides/.*deploy", r"/guides/kube-deploy", r"/guides/swarm-deploy"],
                        "max_pages": 20
                    }
                }
            },
            "02_devops": {
                "description": "CI/CD and development workflows",
                "sections": {
                    "cicd_integration": {
                        "url": "https://docs.docker.com/guides/gha/",
                        "patterns": [r"/guides/gha", r"/guides/azure-pipelines", r"/guides/.*ci"],
                        "max_pages": 15
                    },
                    "desktop": {
                        "url": "https://docs.docker.com/desktop/",
                        "patterns": [r"/desktop/"],
                        "max_pages": 20
                    },
                    "build_cloud": {
                        "url": "https://docs.docker.com/build-cloud/",
                        "patterns": [r"/build-cloud/"],
                        "max_pages": 15
                    }
                }
            },
            "03_security_enterprise": {
                "description": "Security and enterprise features",
                "sections": {
                    "security": {
                        "url": "https://docs.docker.com/security/",
                        "patterns": [r"/security/"],
                        "max_pages": 20
                    },
                    "scout": {
                        "url": "https://docs.docker.com/scout/",
                        "patterns": [r"/scout/"],
                        "max_pages": 15
                    }
                }
            },
            "04_guides": {
                "description": "Language and technology specific guides",
                "sections": {
                    "languages": {
                        "url": "https://docs.docker.com/guides/language/",
                        "patterns": [r"/guides/language/", r"/guides/python", r"/guides/nodejs", r"/guides/java", r"/guides/golang"],
                        "max_pages": 25
                    },
                    "best_practices": {
                        "url": "https://docs.docker.com/guides/best-practices/",
                        "patterns": [r"/guides/best-practices", r"/guides/production"],
                        "max_pages": 15
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
        path_parts = [part for part in url.split('/') if part and part != 'docs.docker.com']
        return '_'.join(path_parts[-2:]) if len(path_parts) >= 2 else path_parts[-1] if path_parts else 'index'
    
    def convert_to_markdown(self, content: str, metadata: Dict[str, Any], url: str) -> str:
        """Convert scraped content to markdown with frontmatter"""
        
        # Create YAML frontmatter
        title = metadata.get('title', 'Docker Documentation').replace('"', '\\"')
        description = metadata.get('description', '').replace('"', '\\"')
        keywords = metadata.get('keywords', '').replace('"', '\\"')
        
        frontmatter = [
            "---",
            f'title: "{title}"',
            f'source_url: "{url}"',
            f'scraped_date: "{datetime.now().isoformat()}"',
            f'description: "{description}"',
        ]
        
        if keywords:
            frontmatter.append(f'keywords: "{keywords}"')
        
        frontmatter.append("---")
        frontmatter.append("")
        
        # Add title if not in content
        if metadata.get('title') and metadata['title'] not in content[:200]:
            content = f"# {metadata['title']}\n\n{content}"
        
        return '\n'.join(frontmatter) + content
    
    async def scrape_section(self, category: str, section_name: str, section_config: Dict[str, Any]) -> Dict[str, Any]:
        """Scrape a specific documentation section"""
        
        print(f"🐳 Scraping {category}/{section_name}: {section_config['url']}")
        
        try:
            result = await self.scraper.traverse_documentation(
                start_url=section_config['url'],
                max_depth=3,
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
                    "scraping_config": section_config
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
        """Scrape all defined documentation sections"""
        
        print("🚀 Starting comprehensive Docker documentation scraping")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"⚙️  Scraping configuration: {self.scraper.delay_between_requests}s delay, max {self.scraper.max_concurrent} concurrent")
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
                "total_pages_scraped": self.total_scraped
            },
            "results_by_category": self.section_results,
            "output_directory": str(self.output_dir)
        }
        
        # Save summary
        summary_path = self.output_dir / "scraping_summary.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print("\n" + "=" * 70)
        print("🎉 Docker Documentation Scraping Complete!")
        print(f"📊 Total pages scraped: {self.total_scraped}")
        print(f"⏱️  Total time: {duration}")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"📋 Summary saved to: {summary_path}")
        
        return summary

async def main():
    """Main scraping orchestration"""
    
    output_dir = "/Users/jasonewillis/Developer/jwRepos/JLWAI/Agents/docs/Docker/"
    
    scraper = DockerDocumentationScraper(output_dir)
    summary = await scraper.scrape_all_sections()
    
    return summary

if __name__ == "__main__":
    summary = asyncio.run(main())
    print(f"\n🏁 Scraping session completed successfully!")
    print(f"📈 Final statistics: {summary['scraping_session']['total_pages_scraped']} pages scraped")