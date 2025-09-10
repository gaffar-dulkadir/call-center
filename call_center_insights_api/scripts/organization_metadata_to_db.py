#!/usr/bin/env python3
"""
Script to update base_analysis_organization_metadata with base_analysis_call_id
Reads analysis files from /calls/out directory and updates organization_metadata table
Uses asyncpg directly without datalayer dependencies
"""

import asyncio
import asyncpg
import json
import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from uuid import UUID

# ---! Add the src directory to the path so we can import config
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import Config


class OrganizationMetadataToDBUpdater:
    """Updater class for processing organization metadata and updating base_analysis_result table"""
    
    def __init__(self):
        self.config = Config()
        self.calls_out_path = Path(__file__).parent.parent / "calls" / "out"
        if not self.calls_out_path.exists():
            raise FileNotFoundError(f"Calls out directory not found: {self.calls_out_path}")
    
    async def get_database_connection(self):
        """Get database connection"""
        try:
            conn = await asyncpg.connect(
                host=self.config.postgres_host,
                port=self.config.postgres_port,
                user=self.config.postgres_user,
                password=self.config.postgres_password,
                database=self.config.postgres_database
            )
            return conn
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            raise
    
    def extract_call_id_from_filename(self, filename: str) -> Optional[str]:
        """Extract call ID (UUID) from analysis filename"""
        # ---! Extract UUID from filename like: agent_name_agent_name_queue_phone_date_UUID_analysis.json
        uuid_pattern = r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})'
        match = re.search(uuid_pattern, filename)
        if match:
            return match.group(1)
        return None
    
    def parse_analysis_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Parse analysis JSON file and extract organization metadata"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # ---! Check if data is a list and has the expected structure
            if not isinstance(data, list) or len(data) == 0:
                print(f"⚠️  Invalid data structure in {file_path.name}")
                return None
            
            first_item = data[0]
            if 'organization_metadata' not in first_item:
                print(f"⚠️  No organization_metadata found in {file_path.name}")
                return None
            
            org_metadata = first_item['organization_metadata']
            
            # ---! Check if organization_metadata is None or empty
            if not org_metadata:
                print(f"⚠️  Organization metadata is empty or None in {file_path.name}")
                return None
            
            # ---! Debug: print the actual organization_metadata string
            print(f"🔍 Processing organization_metadata: {org_metadata[:200]}...")
            
            # ---! Parse the organization_metadata string to extract relevant information
            # ---! Format: "org_id=301271899 org_tel='5302392138' marka='NUR TİCARET' sektor='Elektrik - Elektronik' sirket_tipi='Şahıs' devices=[] services=[...] kiva=[]"
            
            # ---! Extract organization name (marka) - handle None case safely
            org_name_match = re.search(r"marka='([^']*)'", org_metadata)
            organization_name = org_name_match.group(1) if org_name_match else ''
            
            # ---! Extract organization type (sirket_tipi) - handle None case safely
            org_type_match = re.search(r"sirket_tipi='([^']*)'", org_metadata)
            organization_type = org_type_match.group(1) if org_type_match else ''
            
            # ---! Extract organization industry (sektor) - handle None case safely
            org_industry_match = re.search(r"sektor='([^']*)'", org_metadata)
            organization_industry = org_industry_match.group(1) if org_industry_match else ''
            
            # ---! Extract organization phone (org_tel) - handle None case safely
            org_phone_match = re.search(r"org_tel='([^']*)'", org_metadata)
            organization_phone = org_phone_match.group(1) if org_phone_match else ''
            
            # ---! Extract organization ID (org_id) - handle None case safely
            org_id_match = re.search(r"org_id=(\d+)", org_metadata)
            organization_id = org_id_match.group(1) if org_id_match else ''
            
            result = {
                'organization_name': organization_name,
                'organization_type': organization_type,
                'organization_industry': organization_industry,
                'organization_phone': organization_phone,
                'organization_id': organization_id
            }
            
            # ---! Debug: print extracted values
            print(f"📋 Extracted values: {result}")
            
            # ---! Check if we have at least some organization data
            has_org_data = any(value for value in result.values())
            if not has_org_data:
                print(f"⚠️  No organization metadata found in {file_path.name}")
                return None
            
            return result
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error in {file_path.name}: {e}")
            return None
        except Exception as e:
            print(f"❌ Error reading {file_path.name}: {e}")
            return None
    
    def scan_analysis_files(self) -> List[tuple[Path, str, Dict[str, Any]]]:
        """Scan all analysis files and return (file_path, call_id, parsed_data) tuples"""
        results = []
        
        # ---! Walk through all date directories
        for date_dir in self.calls_out_path.iterdir():
            if not date_dir.is_dir():
                continue
            
            print(f"📁 Scanning directory: {date_dir.name}")
            
            # ---! Process all analysis files in the date directory
            for file_path in date_dir.glob("*_analysis.json"):
                call_id = self.extract_call_id_from_filename(file_path.name)
                if not call_id:
                    print(f"⚠️  Could not extract call ID from filename: {file_path.name}")
                    continue
                
                parsed_data = self.parse_analysis_file(file_path)
                if parsed_data:
                    results.append((file_path, call_id, parsed_data))
                    print(f"✅ Parsed: {file_path.name} -> {call_id}")
                else:
                    print(f"❌ Failed to parse: {file_path.name}")
        
        return results
    
    async def update_database(self, conn, results: List[tuple[Path, str, Dict[str, Any]]]) -> None:
        """Update organization metadata in base_analysis_result table"""
        if not results:
            print("ℹ️  No results to update")
            return
        
        success_count = 0
        error_count = 0
        
        for file_path, call_id, data in results:
            try:
                # ---! Check if base_analysis_result record exists
                check_sql = """
                SELECT 1 FROM call_center_insight.base_analysis_result 
                WHERE base_analysis_call_id = $1
                """
                existing = await conn.fetchval(check_sql, call_id)
                
                if not existing:
                    print(f"⚠️  Base analysis result record not found for {call_id}, skipping...")
                    continue
                
                # ---! Check if organization metadata already exists
                check_org_sql = """
                SELECT base_analysis_organization_metadata FROM call_center_insight.base_analysis_result 
                WHERE base_analysis_call_id = $1
                """
                existing_org_metadata = await conn.fetchval(check_org_sql, call_id)
                
                if existing_org_metadata:
                    print(f"⚠️  Organization metadata already exists for {call_id}, skipping...")
                    continue
                
                # ---! Update the organization metadata column
                update_sql = """
                UPDATE call_center_insight.base_analysis_result 
                SET base_analysis_organization_metadata = $2
                WHERE base_analysis_call_id = $1
                """
                
                # ---! Convert the extracted data to JSONB format
                org_metadata_json = {
                    'organization_name': data['organization_name'],
                    'organization_type': data['organization_type'],
                    'organization_industry': data['organization_industry'],
                    'organization_phone': data['organization_phone'],
                    'organization_id': data['organization_id']
                }
                
                # ---! Convert Python dict to JSON string for asyncpg
                org_metadata_json_string = json.dumps(org_metadata_json)
                
                await conn.execute(update_sql, call_id, org_metadata_json_string)
                
                success_count += 1
                print(f"✅ Updated organization metadata: {call_id}")
                
            except Exception as e:
                error_count += 1
                print(f"❌ Error updating organization metadata for {call_id}: {e}")
        
        print(f"\n📊 Summary: {success_count} successful, {error_count} errors")
    
    async def run(self) -> None:
        """Main execution method"""
        print("🚀 Starting organization metadata to database update...")
        
        try:
            # ---! Get database connection
            conn = await self.get_database_connection()
            
            try:
                # ---! Scan and parse all analysis files
                print("🔍 Scanning analysis files for organization metadata...")
                results = self.scan_analysis_files()
                
                if not results:
                    print("ℹ️  No analysis files with organization metadata found to process")
                    return
                
                print(f"📋 Found {len(results)} analysis files with organization metadata to process")
                
                # ---! Update organization metadata in base_analysis_result table
                print("💾 Updating organization metadata in base_analysis_result table...")
                await self.update_database(conn, results)
                
                print("✅ Organization metadata update completed successfully!")
                
            finally:
                await conn.close()
                print("🔌 Database connection closed")
            
        except Exception as e:
            print(f"❌ Fatal error: {e}")
            raise


async def main():
    """Main entry point"""
    try:
        updater = OrganizationMetadataToDBUpdater()
        await updater.run()
    except KeyboardInterrupt:
        print("\n⏹️  Process interrupted by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
