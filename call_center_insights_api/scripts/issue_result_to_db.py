#!/usr/bin/env python3
"""
Script to convert issue analysis results from JSON files to database
Reads analysis files from /calls/out directory and inserts into issue_analysis_result table
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


class IssueResultToDBConverter:
    """Converter class for processing issue analysis results and inserting into database"""
    
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
        """Parse analysis JSON file and extract issue-specific data"""
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
            
            # ---! Check if this is an issue call
            if insights.get('issue_sub_category') is None:
                print(f"ℹ️  Skipping non-issue call in {file_path.name}")
                return None
            
            # ---! Extract required issue fields
            result = {
                'issue_sub_category': insights.get('issue_sub_category', ''),
                'sub_issue_type': insights.get('sub_issue_type', ''),
                'churn_risk': insights.get('churn_risk', 0),
                'urgency_level': insights.get('urgency_level', ''),
                'related_with_previous_call': insights.get('related_with_previous_call', False),
                'related_with_previous_call_detail': insights.get('related_with_previous_call_detail', '')
            }
            
            # ---! Validate required fields
            if not result['issue_sub_category'] or not result['sub_issue_type'] or not result['urgency_level']:
                print(f"⚠️  Missing required issue fields in {file_path.name}")
                return None
            
            # ---! Validate churn_risk is a valid integer
            if not isinstance(result['churn_risk'], int) or result['churn_risk'] < 0 or result['churn_risk'] > 10:
                print(f"⚠️  Invalid churn_risk value in {file_path.name}: {result['churn_risk']}")
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
                if parsed_data is not None:
                    results.append((file_path, call_id, parsed_data))
                    print(f"✅ Parsed issue: {file_path.name} -> {call_id}")
                else:
                    print(f"❌ Failed to parse: {file_path.name}")
        
        return results
    
    async def insert_into_database(self, conn, results: List[tuple[Path, str, Dict[str, Any]]]) -> None:
        """Insert parsed issue results into database"""
        if not results:
            print("ℹ️  No issue results to insert")
            return
        
        success_count = 0
        error_count = 0
        
        for file_path, call_id, data in results:
            try:
                # ---! Check if record already exists
                check_sql = """
                SELECT 1 FROM call_center_insight.issue_analysis_result 
                WHERE issue_analysis_id = $1
                """
                existing = await conn.fetchval(check_sql, call_id)
                
                if existing:
                    print(f"⚠️  Issue record already exists for {call_id}, skipping...")
                    continue
                
                # ---! Check if base analysis result exists (foreign key constraint)
                base_check_sql = """
                SELECT 1 FROM call_center_insight.base_analysis_result 
                WHERE base_analysis_call_id = $1
                """
                base_exists = await conn.fetchval(base_check_sql, call_id)
                
                if not base_exists:
                    print(f"⚠️  Base analysis result not found for {call_id}, skipping...")
                    continue
                
                # ---! Insert new issue record
                insert_sql = """
                INSERT INTO call_center_insight.issue_analysis_result (
                    issue_analysis_id,
                    issue_analysis_sub_category,
                    issue_analysis_sub_issue_type,
                    issue_analysis_churn_risk,
                    issue_analysis_urgency_level,
                    issue_analysis_related_with_previous_call,
                    issue_analysis_related_with_previous_call_detail
                ) VALUES ($1, $2, $3, $4, $5, $6, $7)
                """
                
                await conn.execute(
                    insert_sql,
                    call_id,
                    data['issue_sub_category'],
                    data['sub_issue_type'],
                    data['churn_risk'],
                    data['urgency_level'],
                    data['related_with_previous_call'],
                    data['related_with_previous_call_detail']
                )
                
                success_count += 1
                print(f"✅ Inserted issue: {call_id}")
                
            except Exception as e:
                error_count += 1
                print(f"❌ Error inserting issue {call_id}: {e}")
        
        print(f"\n📊 Summary: {success_count} successful, {error_count} errors")
    
    async def run(self) -> None:
        """Main execution method"""
        print("🚀 Starting issue result to database conversion...")
        
        try:
            # ---! Get database connection
            conn = await self.get_database_connection()
            
            try:
                # ---! Scan and parse all analysis files
                print("🔍 Scanning analysis files for issues...")
                results = self.scan_analysis_files()
                
                if not results:
                    print("ℹ️  No issue analysis files found to process")
                    return
                
                print(f"📋 Found {len(results)} issue analysis files to process")
                
                # ---! Insert results into database
                print("💾 Inserting issue results into database...")
                await self.insert_into_database(conn, results)
                
                print("✅ Issue conversion completed successfully!")
                
            finally:
                await conn.close()
                print("🔌 Database connection closed")
            
        except Exception as e:
            print(f"❌ Fatal error: {e}")
            raise


async def main():
    """Main entry point"""
    try:
        converter = IssueResultToDBConverter()
        await converter.run()
    except KeyboardInterrupt:
        print("\n⏹️  Process interrupted by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
