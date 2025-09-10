#!/usr/bin/env python3
"""
Script to import conversation data from text files into PostgreSQL database.
Extracts data from /calls/conversations/*/*.txt files and inserts into conversations table.
"""

import os
import re
import asyncio
import asyncpg
from datetime import datetime
import pytz
from pathlib import Path
import sys

# ---! Add the src directory to the path so we can import config
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import Config

class ConversationImporter:
    def __init__(self):
        self.config = Config()
        self.istanbul_tz = pytz.timezone('Europe/Istanbul')
        
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
            
    def parse_conversation_file(self, file_path):
        """Parse a conversation text file and extract relevant data"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # ---! Extract data using regex patterns
            data = {}
            
            # ---! Agent Name
            agent_match = re.search(r'AgentName:\s*(.+)', content)
            if agent_match:
                data['agent_name'] = agent_match.group(1).strip()
            
            # ---! Phone Number (remove leading 0)
            phone_match = re.search(r'PhoneNumber:\s*(.+)', content)
            if phone_match:
                phone = phone_match.group(1).strip()
                # ---! Remove leading 0 if present
                if phone.startswith('0'):
                    phone = phone[1:]
                data['phone_number'] = phone
            
            # ---! Call ID
            call_id_match = re.search(r'CallId:\s*(.+)', content)
            if call_id_match:
                data['call_id'] = call_id_match.group(1).strip()
            
            # ---! Start Date (convert to timestamp with timezone)
            start_date_match = re.search(r'StartDate:\s*(.+)', content)
            if start_date_match:
                date_str = start_date_match.group(1).strip()
                try:
                    # ---! Parse date format: 24.07.2025 23:03:10
                    date_obj = datetime.strptime(date_str, '%d.%m.%Y %H:%M:%S')
                    # ---! Localize to Istanbul timezone
                    istanbul_date = self.istanbul_tz.localize(date_obj)
                    data['start_date'] = istanbul_date
                except ValueError as e:
                    print(f"⚠️  Could not parse date '{date_str}' from {file_path}: {e}")
                    return None
            
            # ---! Duration
            duration_match = re.search(r'Duration:\s*([\d.]+)', content)
            if duration_match:
                data['duration'] = float(duration_match.group(1))
            
            # ---! Agent Speech Rate
            agent_speech_match = re.search(r'Agent Speech Rate:\s*%?([\d.]+)', content)
            if agent_speech_match:
                data['agent_speech_rate'] = float(agent_speech_match.group(1))
            
            # ---! Customer Speech Rate
            customer_speech_match = re.search(r'Customer Speech Rate:\s*%?([\d.]+)', content)
            if customer_speech_match:
                data['customer_speech_rate'] = float(customer_speech_match.group(1))
            
            # ---! Silence Rate
            silence_match = re.search(r'Silence Rate:\s*%?([\d.]+)', content)
            if silence_match:
                data['silence_rate'] = float(silence_match.group(1))
            
            # ---! Cross Talk Rate
            cross_talk_match = re.search(r'Cross Talk Rate:\s*%?([\d.]+)', content)
            if cross_talk_match:
                data['cross_talk_rate'] = float(cross_talk_match.group(1))
            
            # ---! Agent Interrupt Count
            interrupt_match = re.search(r'Agent Interrupt Count:\s*(\d+)', content)
            if interrupt_match:
                data['agent_interrupt_count'] = int(interrupt_match.group(1))
            
            # ---! Validate required fields
            required_fields = ['agent_name', 'phone_number', 'call_id', 'start_date']
            for field in required_fields:
                if field not in data or data[field] is None:
                    print(f"⚠️  Missing required field '{field}' in {file_path}")
                    return None
                    
            return data
            
        except Exception as e:
            print(f"❌ Error parsing {file_path}: {e}")
            return None
    
    async def insert_conversation(self, conn, data):
        """Insert conversation data into database"""
        try:
            print(data)
            insert_sql = """
            INSERT INTO call_center_insight.conversation (
                conversation_call_id, 
                conversation_agent_name, 
                conversation_phone_number, 
                conversation_created_at, 
                conversation_duration,
                conversation_agent_speech_rate, 
                conversation_customer_speech_rate, 
                conversation_silence_rate,
                conversation_cross_talk_rate, 
                conversation_agent_interrupt_count
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            ON CONFLICT (conversation_call_id) DO UPDATE SET
                conversation_agent_name = EXCLUDED.conversation_agent_name,
                conversation_phone_number = EXCLUDED.conversation_phone_number,
                conversation_created_at = EXCLUDED.conversation_created_at,
                conversation_duration = EXCLUDED.conversation_duration,
                conversation_agent_speech_rate = EXCLUDED.conversation_agent_speech_rate,
                conversation_customer_speech_rate = EXCLUDED.conversation_customer_speech_rate,
                conversation_silence_rate = EXCLUDED.conversation_silence_rate,
                conversation_cross_talk_rate = EXCLUDED.conversation_cross_talk_rate,
                conversation_agent_interrupt_count = EXCLUDED.conversation_agent_interrupt_count
            """
            
            await conn.execute(
                insert_sql,
                data['call_id'],
                data['agent_name'],
                data['phone_number'],
                data['start_date'],
                data.get('duration'),
                data.get('agent_speech_rate'),
                data.get('customer_speech_rate'),
                data.get('silence_rate'),
                data.get('cross_talk_rate'),
                data.get('agent_interrupt_count')
            )
            return True
            
        except Exception as e:
            print(f"❌ Error inserting conversation {data.get('call_id', 'unknown')}: {e}")
            return False
    
    def find_conversation_files(self, base_path):
        """Find all conversation text files recursively"""
        conversation_files = []
        base_path = Path(base_path)
        
        if not base_path.exists():
            print(f"❌ Base path does not exist: {base_path}")
            return conversation_files
            
        # ---! Search for .txt files in all subdirectories
        for txt_file in base_path.rglob("*.txt"):
            conversation_files.append(txt_file)
            
        return conversation_files
    
    async def import_conversations(self):
        """Main method to import all conversations"""
        print("🚀 Starting conversation import process...")
        
        # ---! Get database connection
        conn = await self.get_database_connection()
        
        try:
            # ---! Find all conversation files
            base_path = Path(__file__).parent.parent / "calls" / "conversations"
            conversation_files = self.find_conversation_files(base_path)
            
            if not conversation_files:
                print("❌ No conversation files found")
                return
                
            print(f"📁 Found {len(conversation_files)} conversation files")
            
            # ---! Process each file
            successful_imports = 0
            failed_imports = 0
            
            for file_path in conversation_files:
                print(f"📄 Processing: {file_path.name}")
                
                # ---! Parse the file
                data = self.parse_conversation_file(file_path)
                
                if data is None:
                    failed_imports += 1
                    continue
                
                # ---! Insert into database
                if await self.insert_conversation(conn, data):
                    successful_imports += 1
                    print(f"✅ Imported: {data['call_id']}")
                else:
                    failed_imports += 1
            
            # ---! Print summary
            print(f"\n📊 Import Summary:")
            print(f"   ✅ Successful imports: {successful_imports}")
            print(f"   ❌ Failed imports: {failed_imports}")
            print(f"   📁 Total files processed: {len(conversation_files)}")
            
        finally:
            await conn.close()
            print("🔌 Database connection closed")

async def main():
    """Main entry point"""
    try:
        importer = ConversationImporter()
        await importer.import_conversations()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
