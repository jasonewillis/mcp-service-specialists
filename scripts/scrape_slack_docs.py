#!/usr/bin/env python3
"""
Slack Documentation Scraper for Fed Job Advisor
Focuses on FREE tier features only - no paid Slack integration
Uses the webscraping MCP agent to scrape Slack documentation
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

class SlackDocumentationScraper:
    """Orchestrates the scraping of Slack documentation focusing on FREE features"""
    
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.scraper = WebscrapingSpecialist()
        
        # Configure scraping for respectful access to Slack docs
        self.scraper.delay_between_requests = 2.0  # 2 seconds between requests
        self.scraper.max_concurrent = 2  # Conservative concurrent limit
        self.scraper.timeout = 45  # Longer timeout for large pages
        
        # Define scraping sections focused on FREE tier features
        self.scraping_sections = {
            "01_free_webhooks": {
                "description": "Incoming Webhooks - FREE feature for sending messages",
                "sections": {
                    "incoming_webhooks": {
                        "url": "https://api.slack.com/messaging/webhooks",
                        "patterns": [
                            r"/messaging/webhooks",
                            r"/incoming-webhooks", 
                            r"/legacy/custom-integrations/incoming-webhooks"
                        ],
                        "max_pages": 15
                    },
                    "webhook_setup": {
                        "url": "https://api.slack.com/apps",
                        "patterns": [
                            r"/apps/quickstart",
                            r"/start/quickstart",
                            r"/authentication/basics"
                        ],
                        "max_pages": 10
                    }
                }
            },
            "02_free_apps": {
                "description": "Slack Apps - FREE basic app features",
                "sections": {
                    "app_basics": {
                        "url": "https://api.slack.com/start",
                        "patterns": [
                            r"/start/",
                            r"/basics/",
                            r"/apps/building"
                        ],
                        "max_pages": 15
                    },
                    "bot_users": {
                        "url": "https://api.slack.com/bot-users",
                        "patterns": [
                            r"/bot-users",
                            r"/concepts/bot-users",
                            r"/methods/chat.postMessage"
                        ],
                        "max_pages": 10
                    }
                }
            },
            "03_free_api_methods": {
                "description": "Web API methods available on FREE tier",
                "sections": {
                    "chat_methods": {
                        "url": "https://api.slack.com/methods/chat.postMessage",
                        "patterns": [
                            r"/methods/chat\.",
                            r"/messaging/sending",
                            r"/messaging/composing"
                        ],
                        "max_pages": 15
                    },
                    "auth_methods": {
                        "url": "https://api.slack.com/methods/auth.test",
                        "patterns": [
                            r"/methods/auth\.",
                            r"/authentication/",
                            r"/methods/api\.test"
                        ],
                        "max_pages": 10
                    }
                }
            },
            "04_message_formatting": {
                "description": "Message formatting and blocks - FREE features",
                "sections": {
                    "block_kit": {
                        "url": "https://api.slack.com/block-kit",
                        "patterns": [
                            r"/block-kit",
                            r"/reference/block-kit",
                            r"/messaging/composing/layouts"
                        ],
                        "max_pages": 20
                    },
                    "markdown": {
                        "url": "https://api.slack.com/reference/surfaces/formatting",
                        "patterns": [
                            r"/surfaces/formatting",
                            r"/messaging/composing/formatting",
                            r"/docs/message-formatting"
                        ],
                        "max_pages": 10
                    }
                }
            },
            "05_rate_limits": {
                "description": "Rate limits and best practices - FREE tier considerations",
                "sections": {
                    "rate_limiting": {
                        "url": "https://api.slack.com/docs/rate-limits",
                        "patterns": [
                            r"/rate-limits",
                            r"/docs/rate-limits",
                            r"/best-practices"
                        ],
                        "max_pages": 10
                    }
                }
            },
            "06_slack_dev_docs": {
                "description": "Developer documentation from docs.slack.dev",
                "sections": {
                    "overview": {
                        "url": "https://docs.slack.dev/",
                        "patterns": [
                            r"docs\.slack\.dev/$",
                            r"docs\.slack\.dev/overview",
                            r"docs\.slack\.dev/getting-started"
                        ],
                        "max_pages": 10
                    },
                    "web_api": {
                        "url": "https://docs.slack.dev/web-api",
                        "patterns": [
                            r"docs\.slack\.dev/web-api",
                            r"docs\.slack\.dev/apis"
                        ],
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
        # Remove domain and clean up
        url_clean = url.replace('https://api.slack.com/', '').replace('https://docs.slack.dev/', '')
        url_clean = url_clean.replace('/', '_').replace('#', '_').replace('?', '_')
        return url_clean or 'index'
    
    def filter_free_content(self, content: str) -> str:
        """Filter out paid/enterprise features from content"""
        # Keywords that indicate paid features
        paid_keywords = [
            'enterprise grid',
            'enterprise key management',
            'paid plan',
            'premium feature',
            'workspace owner',
            'slack connect',
            'enterprise mobility',
            'data loss prevention',
            'audit logs api',
            'discovery api',
            'scim api',
            'enterprise administration'
        ]
        
        # Simple filtering - in production would be more sophisticated
        lines = content.split('\n')
        filtered_lines = []
        skip_section = False
        
        for line in lines:
            line_lower = line.lower()
            # Check if we're entering a paid section
            if any(keyword in line_lower for keyword in paid_keywords):
                skip_section = True
            # Check for section headers that might end paid section
            elif line.startswith('#') or line.startswith('##'):
                skip_section = False
                # But check if this new section is also paid
                if any(keyword in line_lower for keyword in paid_keywords):
                    skip_section = True
            
            if not skip_section:
                filtered_lines.append(line)
        
        return '\n'.join(filtered_lines)
    
    def convert_to_markdown(self, content: str, metadata: Dict[str, Any], url: str) -> str:
        """Convert scraped content to markdown with frontmatter"""
        
        # Filter out paid features
        filtered_content = self.filter_free_content(content)
        
        # Create YAML frontmatter
        title = metadata.get('title', 'Slack Documentation').replace('"', '\\"')
        description = metadata.get('description', '').replace('"', '\\"')
        keywords = metadata.get('keywords', '').replace('"', '\\"')
        
        frontmatter = [
            "---",
            f'title: "{title}"',
            f'source_url: "{url}"',
            f'scraped_date: "{datetime.now().isoformat()}"',
            f'description: "{description}"',
            'tier: "FREE"',
            'category: "slack_integration"'
        ]
        
        if keywords:
            frontmatter.append(f'keywords: "{keywords}"')
        
        # Add FREE tier notice
        frontmatter.append('note: "Documentation filtered for FREE tier features only"')
        
        frontmatter.append("---")
        frontmatter.append("")
        
        # Add title if not in content
        if metadata.get('title') and metadata['title'] not in filtered_content[:200]:
            filtered_content = f"# {metadata['title']}\n\n{filtered_content}"
        
        # Add FREE tier reminder
        filtered_content = f"**Note: This documentation covers FREE tier features only**\n\n{filtered_content}"
        
        return '\n'.join(frontmatter) + filtered_content
    
    async def scrape_section(self, category: str, section_name: str, section_config: Dict[str, Any]) -> Dict[str, Any]:
        """Scrape a specific documentation section"""
        
        print(f"💬 Scraping {category}/{section_name}: {section_config['url']}")
        
        try:
            result = await self.scraper.traverse_documentation(
                start_url=section_config['url'],
                max_depth=2,  # Shallower depth for Slack docs
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
                    "tier": "FREE",
                    "note": "Focused on FREE tier Slack features only"
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
        """Scrape all defined Slack documentation sections"""
        
        print("🚀 Starting Slack documentation scraping (FREE tier features only)")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"⚙️  Scraping configuration: {self.scraper.delay_between_requests}s delay, max {self.scraper.max_concurrent} concurrent")
        print("💡 Focus: FREE tier features - Webhooks, Basic Apps, Web API")
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
                "focus": "FREE tier Slack features only",
                "excluded": "Enterprise Grid, Paid Plans, Premium Features"
            },
            "results_by_category": self.section_results,
            "output_directory": str(self.output_dir),
            "free_features_covered": [
                "Incoming Webhooks",
                "Basic Slack Apps",
                "Bot Users",
                "Web API (chat.postMessage, auth.test)",
                "Block Kit",
                "Message Formatting",
                "Rate Limits"
            ]
        }
        
        # Save summary
        summary_path = self.output_dir / "scraping_summary.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print("\n" + "=" * 70)
        print("🎉 Slack Documentation Scraping Complete!")
        print(f"📊 Total pages scraped: {self.total_scraped}")
        print(f"⏱️  Total time: {duration}")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"📋 Summary saved to: {summary_path}")
        print("💡 Coverage: FREE tier features only - no paid Slack integration required")
        
        return summary

async def main():
    """Main scraping orchestration"""
    
    output_dir = "/Users/jasonewillis/Developer/jwRepos/JLWAI/Agents/docs/Slack/"
    
    scraper = SlackDocumentationScraper(output_dir)
    summary = await scraper.scrape_all_sections()
    
    return summary

if __name__ == "__main__":
    summary = asyncio.run(main())
    print(f"\n🏁 Slack FREE tier documentation scraping completed successfully!")
    print(f"📈 Final statistics: {summary['scraping_session']['total_pages_scraped']} pages scraped")