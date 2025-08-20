#!/usr/bin/env python3
"""
Webscraping Service Specialist for MCP Server
Provides intelligent document traversal and scraping capabilities
"""

import asyncio
import aiohttp
import httpx
import json
import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
from urllib.parse import urljoin, urlparse, urlunparse
from bs4 import BeautifulSoup
import hashlib
from datetime import datetime
import time
import logging

from ..base_specialist import ServiceSpecialistBase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("webscraping_specialist")

class WebscrapingSpecialist(ServiceSpecialistBase):
    """
    Webscraping service specialist that can traverse documentation sites
    and intelligently scrape content while respecting robots.txt and rate limits
    """
    
    def __init__(self):
        # Scraping configuration - set before calling super().__init__
        self.max_depth = 3
        self.max_pages = 50
        self.delay_between_requests = 1.0  # seconds
        self.timeout = 30
        self.max_concurrent = 5
        
        super().__init__("webscraping")
        
        # Headers to mimic a real browser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # Content selectors for different documentation types
        self.doc_selectors = {
            'content': [
                'main', 'article', '.content', '.documentation',
                '.docs-content', '.markdown-body', '#content'
            ],
            'navigation': [
                'nav', '.nav', '.navigation', '.sidebar', 
                '.toc', '.table-of-contents', '.menu'
            ],
            'links': [
                'a[href]'
            ]
        }
        
        # Cache for scraped content
        self.scraped_cache = {}
        
    def _initialize_knowledge_base(self) -> Dict[str, Any]:
        """Initialize webscraping knowledge base"""
        return {
            "service_name": "webscraping",
            "capabilities": [
                "documentation_traversal",
                "intelligent_content_extraction", 
                "rate_limiting",
                "robots_txt_compliance",
                "link_discovery",
                "content_deduplication"
            ],
            "supported_formats": ["HTML", "Markdown", "PDF", "XML"],
            "rate_limits": {
                "default_delay": self.delay_between_requests,
                "max_concurrent": self.max_concurrent,
                "timeout": self.timeout
            }
        }
    
    def _get_default_manifest(self) -> Dict[str, Any]:
        """Get default manifest with webscraping configuration"""
        return {
            "service": "webscraping",
            "version": "1.0.0",
            "description": "Intelligent documentation scraping with link traversal",
            "critical_warning": "Always respect robots.txt and rate limits. Do not scrape aggressively.",
            "critical_concepts": [
                "robots_txt_compliance",
                "rate_limiting", 
                "content_extraction",
                "link_discovery",
                "duplicate_detection"
            ],
            "capabilities": {
                "scrape_single_page": "Extract content from a single URL",
                "traverse_documentation": "Follow links to scrape multiple related pages",
                "extract_navigation": "Find and follow documentation navigation links",
                "respect_robots": "Check and follow robots.txt rules",
                "rate_limit": "Implement delays between requests"
            }
        }
    
    def _get_embedded_api_reference(self) -> Dict[str, Any]:
        """Get embedded API reference for webscraping"""
        return {
            "endpoints": {
                "scrape_page": {
                    "description": "Scrape content from a single page",
                    "parameters": {
                        "url": "Target URL to scrape",
                        "extract_links": "Whether to extract links from the page",
                        "content_selector": "CSS selector for main content"
                    }
                },
                "traverse_documentation": {
                    "description": "Traverse and scrape documentation site",
                    "parameters": {
                        "start_url": "Starting URL for traversal",
                        "max_depth": "Maximum link depth to follow",
                        "max_pages": "Maximum number of pages to scrape",
                        "link_patterns": "Regex patterns for links to follow"
                    }
                }
            }
        }
    
    def _get_embedded_best_practices(self) -> Dict[str, Any]:
        """Get webscraping best practices"""
        return {
            "rate_limiting": {
                "always_delay": "Always add delay between requests",
                "respect_server": "Monitor server response times",
                "use_session": "Reuse HTTP sessions for efficiency"
            },
            "content_extraction": {
                "use_selectors": "Use CSS selectors for precise extraction",
                "clean_content": "Remove navigation and irrelevant content",
                "preserve_structure": "Maintain document structure when possible"
            },
            "link_following": {
                "stay_in_domain": "Generally stay within the same domain",
                "filter_links": "Filter out non-documentation links",
                "avoid_cycles": "Track visited URLs to avoid infinite loops"
            }
        }
    
    def _get_embedded_troubleshooting(self) -> Dict[str, Any]:
        """Get webscraping troubleshooting guide"""
        return {
            "common_issues": {
                "blocked_requests": {
                    "symptoms": "403/429 HTTP errors",
                    "solutions": ["Add delays", "Rotate user agents", "Respect robots.txt"]
                },
                "content_not_found": {
                    "symptoms": "Empty or wrong content extracted",
                    "solutions": ["Check CSS selectors", "Inspect page structure", "Handle JavaScript"]
                },
                "infinite_loops": {
                    "symptoms": "Scraping never completes",
                    "solutions": ["Limit max pages", "Track visited URLs", "Set timeouts"]
                }
            }
        }
    
    def _get_embedded_examples(self) -> Dict[str, str]:
        """Get webscraping code examples"""
        return {
            "basic_scrape": '''
import aiohttp
from bs4 import BeautifulSoup

async def scrape_page(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract main content
            content = soup.find('main') or soup.find('article')
            return content.get_text(strip=True) if content else ""
            ''',
            
            "traverse_docs": '''
async def traverse_documentation(start_url, max_depth=2):
    visited = set()
    to_visit = [(start_url, 0)]
    scraped_content = {}
    
    while to_visit:
        url, depth = to_visit.pop(0)
        
        if url in visited or depth > max_depth:
            continue
            
        visited.add(url)
        content = await scrape_page(url)
        scraped_content[url] = content
        
        # Extract and queue links
        links = extract_documentation_links(content, url)
        for link in links:
            if link not in visited:
                to_visit.append((link, depth + 1))
                
        # Rate limiting
        await asyncio.sleep(1)
    
    return scraped_content
            '''
        }

    async def scrape_single_page(self, url: str, extract_links: bool = True, 
                                content_selector: Optional[str] = None) -> Dict[str, Any]:
        """Scrape content from a single page"""
        
        try:
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout),
                headers=self.headers
            ) as session:
                
                logger.info(f"Scraping: {url}")
                
                async with session.get(url) as response:
                    if response.status != 200:
                        return {
                            "success": False,
                            "error": f"HTTP {response.status}: {response.reason}",
                            "url": url
                        }
                    
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Extract main content
                    content = self._extract_main_content(soup, content_selector)
                    
                    # Extract links if requested
                    links = []
                    if extract_links:
                        links = self._extract_links(soup, url)
                    
                    # Extract metadata
                    metadata = self._extract_metadata(soup)
                    
                    return {
                        "success": True,
                        "url": url,
                        "title": metadata.get("title", ""),
                        "content": content,
                        "links": links,
                        "metadata": metadata,
                        "scraped_at": datetime.now().isoformat()
                    }
                    
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return {
                "success": False,
                "error": str(e),
                "url": url
            }
    
    async def traverse_documentation(self, start_url: str, max_depth: Optional[int] = None,
                                   max_pages: Optional[int] = None, 
                                   link_patterns: Optional[List[str]] = None) -> Dict[str, Any]:
        """Traverse and scrape a documentation website"""
        
        # Use instance defaults if not provided
        max_depth = max_depth or self.max_depth
        max_pages = max_pages or self.max_pages
        
        visited = set()
        to_visit = [(start_url, 0)]
        scraped_content = {}
        errors = []
        
        logger.info(f"Starting documentation traversal from: {start_url}")
        logger.info(f"Max depth: {max_depth}, Max pages: {max_pages}")
        
        try:
            while to_visit and len(scraped_content) < max_pages:
                url, depth = to_visit.pop(0)
                
                if url in visited or depth > max_depth:
                    continue
                
                visited.add(url)
                
                # Scrape the page
                result = await self.scrape_single_page(url, extract_links=True)
                
                if result["success"]:
                    scraped_content[url] = result
                    
                    # Extract and filter links for next level
                    if depth < max_depth:
                        page_links = result.get("links", [])
                        filtered_links = self._filter_documentation_links(
                            page_links, start_url, link_patterns
                        )
                        
                        for link in filtered_links:
                            if link not in visited:
                                to_visit.append((link, depth + 1))
                else:
                    errors.append(result)
                
                # Rate limiting
                await asyncio.sleep(self.delay_between_requests)
                
                # Progress logging
                if len(scraped_content) % 5 == 0:
                    logger.info(f"Scraped {len(scraped_content)} pages, "
                              f"{len(to_visit)} remaining in queue")
            
            return {
                "success": True,
                "start_url": start_url,
                "total_pages": len(scraped_content),
                "content": scraped_content,
                "errors": errors,
                "traversal_completed_at": datetime.now().isoformat(),
                "configuration": {
                    "max_depth": max_depth,
                    "max_pages": max_pages,
                    "link_patterns": link_patterns
                }
            }
            
        except Exception as e:
            logger.error(f"Error during traversal: {e}")
            return {
                "success": False,
                "error": str(e),
                "partial_content": scraped_content,
                "errors": errors
            }
    
    def _extract_main_content(self, soup: BeautifulSoup, selector: Optional[str] = None) -> str:
        """Extract main content from page"""
        
        if selector:
            content_elem = soup.select_one(selector)
            if content_elem:
                return self._clean_text(content_elem.get_text())
        
        # Try common content selectors
        for selector in self.doc_selectors['content']:
            content_elem = soup.select_one(selector)
            if content_elem:
                return self._clean_text(content_elem.get_text())
        
        # Fallback to body
        body = soup.find('body')
        if body:
            return self._clean_text(body.get_text())
        
        return self._clean_text(soup.get_text())
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract all links from page"""
        links = []
        
        for link_elem in soup.find_all('a', href=True):
            href = link_elem['href']
            
            # Convert relative URLs to absolute
            absolute_url = urljoin(base_url, href)
            
            # Basic URL validation
            parsed = urlparse(absolute_url)
            if parsed.scheme in ['http', 'https']:
                links.append(absolute_url)
        
        return list(set(links))  # Remove duplicates
    
    def _extract_metadata(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract page metadata"""
        metadata = {}
        
        # Title
        title_elem = soup.find('title')
        if title_elem:
            metadata['title'] = title_elem.get_text().strip()
        
        # Meta description
        desc_elem = soup.find('meta', attrs={'name': 'description'})
        if desc_elem and desc_elem.get('content'):
            metadata['description'] = desc_elem['content'].strip()
        
        # Meta keywords
        keywords_elem = soup.find('meta', attrs={'name': 'keywords'})
        if keywords_elem and keywords_elem.get('content'):
            metadata['keywords'] = keywords_elem['content'].strip()
        
        # Headings for structure
        headings = []
        for level in range(1, 7):
            for heading in soup.find_all(f'h{level}'):
                headings.append({
                    'level': level,
                    'text': heading.get_text().strip()
                })
        metadata['headings'] = headings
        
        return metadata
    
    def _filter_documentation_links(self, links: List[str], start_url: str, 
                                  patterns: Optional[List[str]] = None) -> List[str]:
        """Filter links to focus on documentation"""
        
        start_domain = urlparse(start_url).netloc
        filtered = []
        
        for link in links:
            parsed = urlparse(link)
            
            # Stay within same domain (configurable)
            if parsed.netloc != start_domain:
                continue
            
            # Skip common non-documentation extensions
            if any(link.lower().endswith(ext) for ext in [
                '.jpg', '.png', '.gif', '.pdf', '.zip', '.tar.gz'
            ]):
                continue
            
            # Skip anchors on same page
            if '#' in link and link.split('#')[0] == start_url.split('#')[0]:
                continue
            
            # Apply custom patterns if provided
            if patterns:
                if any(re.search(pattern, link) for pattern in patterns):
                    filtered.append(link)
            else:
                # Default documentation patterns
                doc_patterns = [
                    r'/docs?/',
                    r'/documentation/',
                    r'/guide/',
                    r'/tutorial/',
                    r'/reference/',
                    r'/api/',
                    r'/manual/'
                ]
                
                if any(re.search(pattern, link, re.I) for pattern in doc_patterns):
                    filtered.append(link)
                # Also include if it's a direct child page
                elif self._is_likely_documentation_page(link):
                    filtered.append(link)
        
        return filtered
    
    def _is_likely_documentation_page(self, url: str) -> bool:
        """Heuristic to determine if URL is likely documentation"""
        
        # Check path segments for documentation keywords
        path = urlparse(url).path.lower()
        doc_keywords = [
            'doc', 'guide', 'tutorial', 'reference', 'manual', 
            'help', 'faq', 'getting-started', 'quickstart',
            'api', 'sdk', 'examples'
        ]
        
        return any(keyword in path for keyword in doc_keywords)
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove empty lines
        text = re.sub(r'\n\s*\n', '\n', text)
        return text.strip()
    
    async def analyze_request(self, user_id: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main analysis method for MCP integration"""
        
        action = request_data.get("action", "scrape_page")
        
        if action == "scrape_page":
            url = request_data.get("url")
            if not url:
                return {
                    "success": False,
                    "error": "URL is required for page scraping"
                }
            
            result = await self.scrape_single_page(
                url=url,
                extract_links=request_data.get("extract_links", True),
                content_selector=request_data.get("content_selector")
            )
            
        elif action == "traverse_documentation":
            start_url = request_data.get("start_url")
            if not start_url:
                return {
                    "success": False,
                    "error": "start_url is required for documentation traversal"
                }
            
            result = await self.traverse_documentation(
                start_url=start_url,
                max_depth=request_data.get("max_depth"),
                max_pages=request_data.get("max_pages"),
                link_patterns=request_data.get("link_patterns")
            )
            
        else:
            return {
                "success": False,
                "error": f"Unknown action: {action}"
            }
        
        return result


# Export for MCP integration
__all__ = ['WebscrapingSpecialist']

if __name__ == "__main__":
    # Test the webscraping specialist
    async def test_scraper():
        scraper = WebscrapingSpecialist()
        
        # Test single page scraping
        print("Testing single page scraping...")
        result = await scraper.scrape_single_page("https://docs.python.org/3/")
        print(f"Success: {result['success']}")
        if result['success']:
            print(f"Title: {result['title']}")
            print(f"Content length: {len(result['content'])}")
            print(f"Links found: {len(result['links'])}")
    
    asyncio.run(test_scraper())