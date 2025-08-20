#!/usr/bin/env python3
"""
Stripe Documentation Scraper for Fed Job Advisor
Focuses on SaaS payment processing for $29 Local and $49 Mobile subscriptions
Uses the webscraping MCP agent to scrape Stripe documentation
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

class StripeDocumentationScraper:
    """Orchestrates the scraping of Stripe documentation for Fed Job Advisor SaaS needs"""
    
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.scraper = WebscrapingSpecialist()
        
        # Configure scraping for respectful access to Stripe docs
        self.scraper.delay_between_requests = 2.0  # 2 seconds between requests
        self.scraper.max_concurrent = 2  # Conservative concurrent limit
        self.scraper.timeout = 45  # Longer timeout for large pages
        
        # Define scraping sections focused on Fed Job Advisor SaaS needs
        self.scraping_sections = {
            "01_subscription_billing": {
                "description": "Subscription billing for Fed Job Advisor pricing tiers",
                "sections": {
                    "subscriptions": {
                        "url": "https://docs.stripe.com/billing/subscriptions/overview",
                        "patterns": [
                            r"/billing/subscriptions/",
                            r"/billing/prices/",
                            r"/billing/products/"
                        ],
                        "max_pages": 15
                    },
                    "pricing_models": {
                        "url": "https://docs.stripe.com/products-prices/overview",
                        "patterns": [
                            r"/products-prices/",
                            r"/billing/subscriptions/checkout/",
                            r"/checkout/quickstart"
                        ],
                        "max_pages": 12
                    }
                }
            },
            "02_payment_integration": {
                "description": "Payment processing integration for web applications",
                "sections": {
                    "checkout_sessions": {
                        "url": "https://docs.stripe.com/checkout/quickstart",
                        "patterns": [
                            r"/checkout/",
                            r"/payments/accept-a-payment/",
                            r"/payments/checkout/"
                        ],
                        "max_pages": 15
                    },
                    "webhooks": {
                        "url": "https://docs.stripe.com/webhooks",
                        "patterns": [
                            r"/webhooks/",
                            r"/webhooks/quickstart",
                            r"/api/webhook_endpoints"
                        ],
                        "max_pages": 10
                    }
                }
            },
            "03_api_integration": {
                "description": "Stripe API integration for Python/JavaScript",
                "sections": {
                    "python_integration": {
                        "url": "https://docs.stripe.com/libraries/python",
                        "patterns": [
                            r"/libraries/python",
                            r"/api/",
                            r"/payments/quickstart"
                        ],
                        "max_pages": 12
                    },
                    "javascript_integration": {
                        "url": "https://docs.stripe.com/js",
                        "patterns": [
                            r"/js/",
                            r"/stripe-js/",
                            r"/elements/"
                        ],
                        "max_pages": 10
                    }
                }
            },
            "04_customer_management": {
                "description": "Customer and subscription management for SaaS",
                "sections": {
                    "customer_portal": {
                        "url": "https://docs.stripe.com/billing/subscriptions/customer-portal",
                        "patterns": [
                            r"/billing/subscriptions/customer-portal",
                            r"/billing/customer-portal/",
                            r"/api/customer_portal"
                        ],
                        "max_pages": 8
                    },
                    "subscription_management": {
                        "url": "https://docs.stripe.com/billing/subscriptions/managing",
                        "patterns": [
                            r"/billing/subscriptions/managing",
                            r"/billing/subscriptions/cancel",
                            r"/billing/subscriptions/pause"
                        ],
                        "max_pages": 10
                    }
                }
            },
            "05_security_compliance": {
                "description": "Security and compliance for federal applications",
                "sections": {
                    "security_best_practices": {
                        "url": "https://docs.stripe.com/security",
                        "patterns": [
                            r"/security/",
                            r"/keys/",
                            r"/api/authentication"
                        ],
                        "max_pages": 8
                    },
                    "testing_integration": {
                        "url": "https://docs.stripe.com/testing",
                        "patterns": [
                            r"/testing/",
                            r"/test-mode/",
                            r"/webhooks/test"
                        ],
                        "max_pages": 6
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
        url_clean = url.replace('https://docs.stripe.com/', '')
        url_clean = url_clean.replace('/', '_').replace('#', '_').replace('?', '_')
        return url_clean or 'index'
    
    def filter_saas_content(self, content: str) -> str:
        """Filter content to focus on SaaS subscription features"""
        # Keywords that indicate relevant SaaS functionality
        saas_keywords = [
            'subscription',
            'billing',
            'customer portal',
            'webhook',
            'recurring',
            'payment method',
            'invoice'
        ]
        
        # Keywords that indicate less relevant content for our use case
        irrelevant_keywords = [
            'marketplace',
            'connect platform',
            'point of sale',
            'terminal',
            'physical goods',
            'shipping'
        ]
        
        lines = content.split('\n')
        filtered_lines = []
        
        for line in lines:
            line_lower = line.lower()
            # De-emphasize irrelevant content
            if any(keyword in line_lower for keyword in irrelevant_keywords):
                if not line.startswith('#'):  # Don't modify headers
                    line = f"<!-- IRRELEVANT: {line} -->"
            # Highlight relevant content
            elif any(keyword in line_lower for keyword in saas_keywords):
                if not line.startswith('#') and not line.startswith('**'):
                    line = f"**{line}**" if line.strip() else line
            
            filtered_lines.append(line)
        
        return '\n'.join(filtered_lines)
    
    def convert_to_markdown(self, content: str, metadata: Dict[str, Any], url: str) -> str:
        """Convert scraped content to markdown with frontmatter"""
        
        # Filter for SaaS focus
        filtered_content = self.filter_saas_content(content)
        
        # Create YAML frontmatter
        title = metadata.get('title', 'Stripe Documentation').replace('"', '\\"')
        description = metadata.get('description', '').replace('"', '\\"')
        keywords = metadata.get('keywords', '').replace('"', '\\"')
        
        frontmatter = [
            "---",
            f'title: "{title}"',
            f'source_url: "{url}"',
            f'scraped_date: "{datetime.now().isoformat()}"',
            f'description: "{description}"',
            'platform: "stripe"',
            'category: "payment_processing"',
            'stack: "fed_job_advisor"',
            'pricing_model: "subscription_saas"'
        ]
        
        if keywords:
            frontmatter.append(f'keywords: "{keywords}"')
        
        # Add Fed Job Advisor context
        frontmatter.append('note: "Documentation focused on Fed Job Advisor SaaS subscription payments ($29 Local, $49 Mobile)"')
        
        frontmatter.append("---")
        frontmatter.append("")
        
        # Add title if not in content
        if metadata.get('title') and metadata['title'] not in filtered_content[:200]:
            filtered_content = f"# {metadata['title']}\n\n{filtered_content}"
        
        # Add Fed Job Advisor context
        filtered_content = f"**Note: This documentation covers Stripe integration for Fed Job Advisor's subscription-based SaaS model**\n\n{filtered_content}"
        
        return '\n'.join(frontmatter) + filtered_content
    
    async def scrape_section(self, category: str, section_name: str, section_config: Dict[str, Any]) -> Dict[str, Any]:
        """Scrape a specific documentation section"""
        
        print(f"💳 Scraping {category}/{section_name}: {section_config['url']}")
        
        try:
            result = await self.scraper.traverse_documentation(
                start_url=section_config['url'],
                max_depth=2,  # Moderate depth for Stripe docs
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
                    "platform": "stripe",
                    "purpose": "Fed Job Advisor SaaS subscription payment processing",
                    "pricing_tiers": ["Local $29/month", "Mobile $49/month"]
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
        """Scrape all defined Stripe documentation sections"""
        
        print("🚀 Starting Stripe documentation scraping for Fed Job Advisor SaaS")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"⚙️  Scraping configuration: {self.scraper.delay_between_requests}s delay, max {self.scraper.max_concurrent} concurrent")
        print("💡 Focus: SaaS subscription payments - Local $29/month, Mobile $49/month")
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
                "focus": "Fed Job Advisor SaaS subscription payment processing",
                "platform": "stripe",
                "pricing_model": "subscription_based"
            },
            "results_by_category": self.section_results,
            "output_directory": str(self.output_dir),
            "fed_job_advisor_features": [
                "Local Tier Subscription ($29/month)",
                "Mobile Tier Subscription ($49/month)", 
                "Customer Portal Management",
                "Subscription Lifecycle Management",
                "Webhook Integration for Payment Events",
                "Python/FastAPI Integration",
                "JavaScript/Next.js Integration",
                "Security Best Practices"
            ]
        }
        
        # Save summary
        summary_path = self.output_dir / "scraping_summary.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print("\n" + "=" * 70)
        print("🎉 Stripe Documentation Scraping Complete!")
        print(f"📊 Total pages scraped: {self.total_scraped}")
        print(f"⏱️  Total time: {duration}")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"📋 Summary saved to: {summary_path}")
        print("💡 Coverage: SaaS subscription payment processing for Fed Job Advisor")
        
        return summary

async def main():
    """Main scraping orchestration"""
    
    output_dir = "/Users/jasonewillis/Developer/jwRepos/JLWAI/Agents/docs/external_services/platforms/stripe/"
    
    scraper = StripeDocumentationScraper(output_dir)
    summary = await scraper.scrape_all_sections()
    
    return summary

if __name__ == "__main__":
    summary = asyncio.run(main())
    print(f"\n🏁 Stripe documentation scraping completed successfully!")
    print(f"📈 Final statistics: {summary['scraping_session']['total_pages_scraped']} pages scraped")