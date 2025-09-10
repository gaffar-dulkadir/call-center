import asyncio
import os
import json
from pathlib import Path
from typing import Dict, Any
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# ---! Import database configuration
import sys
sys.path.append(str(Path(__file__).parent.parent))
from database_config import DATABASE_URL

def get_script_dir() -> Path:
    """Get the directory where this script is located"""
    return Path(__file__).parent

def get_project_root() -> Path:
    """Get the project root directory (parent of scripts directory)"""
    return get_script_dir().parent

async def json_to_db_model(session: AsyncSession, json_data: Dict[str, Any]) -> bool:
    """Insert JSON data into the base_analysis_result table"""
    try:
        # ---! Extract data from the actual JSON structure
        insights = json_data.get("insights", {})
        organization_metadata = json_data.get("organization_metadata", "")
        
        # ---! Extract call reason and details from insights
        call_reason = insights.get("call_reason", "")
        call_reason_detail = insights.get("call_reason_detail", "")
        is_follow_up_required = insights.get("is_follow_up_required", False)
        
        # ---! Generate a unique ID for this analysis (using organization metadata hash)
        import hashlib
        base_analysis_id = hashlib.md5(organization_metadata.encode()).hexdigest()[:16]
        
        # ---! Create SQL query
        query = f"""
        INSERT INTO base_analysis_result (base_analysis_id, base_analysis_reason, base_analysis_reason_detail, base_analysis_call_requires_followup)
        VALUES ('{base_analysis_id}', '{call_reason}', '{call_reason_detail}', {is_follow_up_required})
        """
        
        await session.execute(text(query))
        await session.commit()
        return True
        
    except Exception as e:
        print(f"Error inserting data: {e}")
        await session.rollback()
        return False

async def process_json_file(session: AsyncSession, file_path: Path) -> bool:
    """Process a single JSON file and insert its data into the database"""
    try:
        # ---! Load JSON content
        with open(file_path, 'r', encoding='utf-8') as f:
            json_content = json.load(f)
        
        # ---! Handle both single objects and arrays
        if isinstance(json_content, list):
            success_count = 0
            for item in json_content:
                if await json_to_db_model(session, item):
                    success_count += 1
            print(f"Processed {success_count}/{len(json_content)} records from {file_path.name}")
            return success_count > 0
        else:
            # ---! Single object
            success = await json_to_db_model(session, json_content)
            if success:
                print(f"Successfully processed {file_path.name}")
            return success
            
    except Exception as e:
        print(f"Error processing {file_path.name}: {e}")
        return False

async def dump_all_json_files_to_db(calls_out_path: Path = None) -> None:
    """Dump all JSON files from calls/out directory to the database"""
    # ---! Get the calls/out directory path
    if calls_out_path is None:
        calls_out_dir = get_project_root() / "calls" / "out"
    else:
        calls_out_dir = Path(calls_out_path)
    
    # ---! Check if directory exists
    if not calls_out_dir.exists():
        print(f"Directory does not exist: {calls_out_dir}")
        return
    
    if not calls_out_dir.is_dir():
        print(f"Path is not a directory: {calls_out_dir}")
        return
    
    # ---! Use database configuration from database_config.py
    print(f"Connecting to database using: {DATABASE_URL}")
    
    try:
        engine = create_async_engine(DATABASE_URL)
        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        
        async with async_session() as session:
            total_files = 0
            successful_files = 0
            failed_files = 0
            
            # ---! Process all date directories
            for item in sorted(calls_out_dir.iterdir()):
                if item.is_dir() and item.name.replace("-", "").isdigit() and len(item.name) == 10:
                    print(f"\nProcessing date directory: {item.name}")
                    
                    # ---! Process JSON files in date directory
                    for file_item in sorted(item.iterdir()):
                        if file_item.is_file() and file_item.suffix == ".json":
                            total_files += 1
                            if await process_json_file(session, file_item):
                                successful_files += 1
                            else:
                                failed_files += 1
            
            print(f"\n=== Summary ===")
            print(f"Total JSON files processed: {total_files}")
            print(f"Successful: {successful_files}")
            print(f"Failed: {failed_files}")
            
    except Exception as e:
        print(f"Database connection error: {e}")
        print("Please check your database configuration in database_config.py")
    finally:
        if 'engine' in locals():
            await engine.dispose()

if __name__ == "__main__":
    # ---! Run the main function
    asyncio.run(dump_all_json_files_to_db())
    