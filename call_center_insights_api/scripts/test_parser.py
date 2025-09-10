#!/usr/bin/env python3
"""
Test script to verify conversation parsing logic without database connection.
"""

import sys
import os
from pathlib import Path

# ---! Add the src directory to the path so we can import config
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from import_conversations_to_db import ConversationImporter

def test_parser():
    """Test the conversation parser with a sample file"""
    importer = ConversationImporter()
    
    # ---! Test with the example file
    test_file = Path(__file__).parent.parent / "calls" / "conversations" / "2025_07_24" / "bahar.ogrunc@ode.al_bahar.ogrunc@ode.al_Havuz Aramaları _800 - Stratejik Müşteriler ve İş Ortakları_05318671534_20250724_dcc558df-8be4-464c-ab19-7f9b3004cee3.txt"
    
    if not test_file.exists():
        print(f"❌ Test file not found: {test_file}")
        return
    
    print(f"🧪 Testing parser with: {test_file.name}")
    print("-" * 50)
    
    # ---! Parse the file
    data = importer.parse_conversation_file(test_file)
    
    if data:
        print("✅ Parsing successful!")
        print("\n📊 Extracted data:")
        for key, value in data.items():
            print(f"   {key}: {value}")
    else:
        print("❌ Parsing failed!")
    
    print("\n" + "=" * 50)
    
    # ---! Test phone number processing
    print("📱 Testing phone number processing:")
    test_numbers = ["05318671534", "05318671534", "5318671534", "05318671534"]
    for phone in test_numbers:
        processed = phone[1:] if phone.startswith('0') else phone
        print(f"   {phone} -> {processed}")

if __name__ == "__main__":
    test_parser()
