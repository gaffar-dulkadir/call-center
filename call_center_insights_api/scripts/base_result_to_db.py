#!/usr/bin/env python3
"""
Script to convert base analysis results from JSON files to database
Reads analysis files from /calls/out directory and inserts into base_analysis_result table
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


class BaseResultToDBConverter:
    """Converter class for processing base analysis results and inserting into database"""
    
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
        """Parse analysis JSON file and extract relevant data"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # ---! Check if data is a list and has the expected structure
            if not isinstance(data, list) or len(data) == 0:
                print(f"⚠️  Invalid data structure in {file_path.name}")
                return None
            
            first_item = data[0]
            if 'insights' not in first_item:
                print(f"⚠️  No insights found in {file_path.name}")
                return None
            
            insights = first_item['insights']
            
            # ---! Extract required fields
            result = {
                'call_reason': insights.get('call_reason', ''),
                'call_reason_detail': insights.get('call_reason_detail', ''),
                'is_follow_up_required': insights.get('is_follow_up_required', False)
            }
            
            # ---! Validate required fields
            if not result['call_reason'] or not result['call_reason_detail']:
                print(f"⚠️  Missing required fields in {file_path.name}")
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
    
    async def insert_into_database(self, conn, results: List[tuple[Path, str, Dict[str, Any]]]) -> None:
        """Insert parsed results into database"""
        if not results:
            print("ℹ️  No results to insert")
            return
        
        success_count = 0
        error_count = 0
        
        for file_path, call_id, data in results:
            try:
                # ---! Check if record already exists
                check_sql = """
                SELECT 1 FROM call_center_insight.base_analysis_result 
                WHERE base_analysis_call_id = $1
                """
                existing = await conn.fetchval(check_sql, call_id)
                
                if existing:
                    print(f"⚠️  Record already exists for {call_id}, skipping...")
                    continue
                
                # ---! Insert new record
                insert_sql = """
                INSERT INTO call_center_insight.base_analysis_result (
                    base_analysis_call_id,
                    base_analysis_reason,
                    base_analysis_reason_detail,
                    base_analysis_call_requires_followup
                ) VALUES ($1, $2, $3, $4)
                """
                
                await conn.execute(
                    insert_sql,
                    call_id,
                    data['call_reason'],
                    data['call_reason_detail'],
                    data['is_follow_up_required']
                )
                
                success_count += 1
                print(f"✅ Inserted: {call_id}")
                
            except Exception as e:
                error_count += 1
                print(f"❌ Error inserting {call_id}: {e}")
        
        print(f"\n📊 Summary: {success_count} successful, {error_count} errors")
    
    async def run(self) -> None:
        """Main execution method"""
        print("🚀 Starting base result to database conversion...")
        
        try:
            # ---! Get database connection
            conn = await self.get_database_connection()
            
            try:
                # ---! Scan and parse all analysis files
                print("🔍 Scanning analysis files...")
                results = self.scan_analysis_files()
                
                if not results:
                    print("ℹ️  No analysis files found to process")
                    return
                
                print(f"📋 Found {len(results)} analysis files to process")
                
                # ---! Insert results into database
                print("💾 Inserting results into database...")
                await self.insert_into_database(conn, results)
                
                print("✅ Conversion completed successfully!")
                
            finally:
                await conn.close()
                print("🔌 Database connection closed")
            
        except Exception as e:
            print(f"❌ Fatal error: {e}")
            raise


async def main():
    """Main entry point"""
    try:
        converter = BaseResultToDBConverter()
        await converter.run()
    except KeyboardInterrupt:
        print("\n⏹️  Process interrupted by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
