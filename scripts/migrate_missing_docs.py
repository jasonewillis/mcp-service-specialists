#!/usr/bin/env python3
"""
Migration script to ensure all documentation from documentation_old/external_services 
is properly migrated to the new docs/ structure
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime

class DocumentationMigrator:
    """Migrates missing documentation from old structure to new structure"""
    
    def __init__(self):
        self.old_base = Path("/Users/jasonewillis/Developer/jwRepos/JLWAI/Agents/documentation_old/external_services")
        self.new_base = Path("/Users/jasonewillis/Developer/jwRepos/JLWAI/Agents/docs/external_services")
        
        # Define the mapping from old structure to new structure
        self.service_mappings = {
            # Platform services
            "cron": "platforms/cron",
            "docker": "platforms/docker", 
            "fastapi": "platforms/fastapi",
            "nextjs": "platforms/nextjs",
            "postgresql": "platforms/postgresql",
            "render": "platforms/render",
            "sentry": "platforms/sentry",
            "stripe": "platforms/stripe",
            
            # API services
            "opm": "apis/opm",
            "usajobs": "apis/usajobs",
            
            # Integration services
            "github": "integrations/github",
            "google_analytics": "integrations/google_analytics",
            "oauth": "integrations/oauth",
            "webscraping": "integrations/webscraping"
        }
        
        self.migrated_services = []
        self.skipped_services = []
        self.merged_services = []
    
    def check_existing_content(self, service_name: str, target_path: Path) -> bool:
        """Check if target already has substantial content"""
        if not target_path.exists():
            return False
        
        # Check for substantial content (scraped docs or multiple files)
        content_indicators = [
            target_path / "scraping_summary.json",  # Scraped content
            target_path / "_section_metadata.json"  # Organized sections
        ]
        
        # Count files in target
        try:
            file_count = len([f for f in target_path.rglob("*") if f.is_file()])
            return file_count > 5  # Has substantial content
        except:
            return False
    
    def merge_critical_files(self, source_path: Path, target_path: Path) -> None:
        """Merge critical files from source to target"""
        critical_files = [
            "CRITICAL_*.md",
            "QUICK_REFERENCE.md", 
            "api_reference.md",
            "*.json"
        ]
        
        print(f"    🔄 Merging critical files from {source_path.name}")
        
        for pattern in critical_files:
            for file in source_path.glob(pattern):
                target_file = target_path / file.name
                if not target_file.exists():
                    shutil.copy2(file, target_file)
                    print(f"      ✅ Copied {file.name}")
                else:
                    print(f"      ⚠️  Skipped {file.name} (already exists)")
    
    def copy_service_structure(self, source_path: Path, target_path: Path) -> None:
        """Copy entire service structure from source to target"""
        print(f"    📁 Copying complete structure from {source_path.name}")
        
        # Create target directory
        target_path.mkdir(parents=True, exist_ok=True)
        
        # Copy all contents
        for item in source_path.iterdir():
            target_item = target_path / item.name
            
            if item.is_dir():
                if not target_item.exists():
                    shutil.copytree(item, target_item)
                    print(f"      📂 Copied directory: {item.name}")
                else:
                    print(f"      ⚠️  Directory exists: {item.name}")
            else:
                if not target_item.exists():
                    shutil.copy2(item, target_item)
                    print(f"      📄 Copied file: {item.name}")
                else:
                    print(f"      ⚠️  File exists: {item.name}")
    
    def migrate_service(self, service_name: str) -> None:
        """Migrate a specific service from old to new structure"""
        
        source_path = self.old_base / service_name
        if not source_path.exists():
            print(f"❌ Source not found: {service_name}")
            return
        
        # Get target path
        target_relative = self.service_mappings.get(service_name, f"platforms/{service_name}")
        target_path = self.new_base / target_relative
        
        print(f"\n🔄 Processing: {service_name}")
        print(f"   Source: {source_path}")
        print(f"   Target: {target_path}")
        
        # Check if target has substantial content
        has_existing_content = self.check_existing_content(service_name, target_path)
        
        if has_existing_content:
            print(f"   📊 Target has substantial content - merging critical files only")
            self.merge_critical_files(source_path, target_path)
            self.merged_services.append(service_name)
        else:
            print(f"   📁 Target is empty/minimal - copying complete structure")
            self.copy_service_structure(source_path, target_path)
            self.migrated_services.append(service_name)
    
    def migrate_special_files(self) -> None:
        """Migrate special files from old structure"""
        
        special_files = [
            "DOCUMENTATION_STRUCTURE.md",
            "download_summary.json"
        ]
        
        print("\n📋 Migrating special files...")
        
        for filename in special_files:
            source_file = self.old_base / filename
            if source_file.exists():
                target_file = self.new_base / filename
                if not target_file.exists():
                    shutil.copy2(source_file, target_file)
                    print(f"   ✅ Copied: {filename}")
                else:
                    print(f"   ⚠️  Already exists: {filename}")
    
    def generate_migration_report(self) -> None:
        """Generate a report of the migration process"""
        
        report = {
            "migration_date": datetime.now().isoformat(),
            "source_directory": str(self.old_base),
            "target_directory": str(self.new_base),
            "services_migrated": self.migrated_services,
            "services_merged": self.merged_services,
            "services_skipped": self.skipped_services,
            "summary": {
                "total_processed": len(self.migrated_services) + len(self.merged_services) + len(self.skipped_services),
                "fully_migrated": len(self.migrated_services),
                "merged_only": len(self.merged_services),
                "skipped": len(self.skipped_services)
            }
        }
        
        report_path = self.new_base / "migration_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📋 Migration report saved to: {report_path}")
        
        # Print summary
        print("\n" + "="*60)
        print("📊 MIGRATION SUMMARY")
        print("="*60)
        print(f"✅ Fully migrated services: {len(self.migrated_services)}")
        if self.migrated_services:
            for service in self.migrated_services:
                print(f"   • {service}")
        
        print(f"\n🔄 Merged with existing: {len(self.merged_services)}")
        if self.merged_services:
            for service in self.merged_services:
                print(f"   • {service}")
        
        print(f"\n⚠️  Skipped services: {len(self.skipped_services)}")
        if self.skipped_services:
            for service in self.skipped_services:
                print(f"   • {service}")
        
        print(f"\n📁 Total services processed: {report['summary']['total_processed']}")
    
    def run_migration(self) -> None:
        """Run the complete migration process"""
        
        print("🚀 Starting documentation migration from old to new structure...")
        print(f"📂 Source: {self.old_base}")
        print(f"📂 Target: {self.new_base}")
        print("="*60)
        
        # Get all services from old structure
        services_to_migrate = [
            item.name for item in self.old_base.iterdir() 
            if item.is_dir() and not item.name.startswith('.')
        ]
        
        print(f"📋 Found {len(services_to_migrate)} services to process:")
        for service in sorted(services_to_migrate):
            print(f"   • {service}")
        
        # Migrate each service
        for service_name in sorted(services_to_migrate):
            try:
                self.migrate_service(service_name)
            except Exception as e:
                print(f"❌ Error migrating {service_name}: {e}")
                self.skipped_services.append(service_name)
        
        # Migrate special files
        self.migrate_special_files()
        
        # Generate report
        self.generate_migration_report()
        
        print("\n🎉 Migration completed!")

if __name__ == "__main__":
    migrator = DocumentationMigrator()
    migrator.run_migration()