# Conversation Import Script

This script imports conversation data from text files into a PostgreSQL database.

## Features

- Extracts data from all `.txt` files in `/calls/conversations/*/` directories
- Parses conversation metadata including:
  - Agent Name
  - Phone Number (removes leading 0)
  - Call ID
  - Start Date (converted to Istanbul timezone)
  - Duration
  - Agent Speech Rate
  - Customer Speech Rate
  - Silence Rate
  - Cross Talk Rate
  - Agent Interrupt Count
- Creates database table automatically
- Handles duplicate entries with upsert logic
- Provides detailed import summary

## Prerequisites

1. PostgreSQL database running
2. Python 3.8+
3. Required Python packages (see requirements.txt)

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment variables in your `.env` file:
   ```bash
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_USER=your_username
   POSTGRES_PASSWORD=your_password
   POSTGRES_DATABASE=your_database
   ```

## Usage

Run the script from the project root directory:

```bash
python scripts/import_conversations_to_db.py
```

## Database Schema

The script creates a `conversations` table with the following structure:

```sql
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    agent_name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    call_id VARCHAR(255) NOT NULL UNIQUE,
    start_date TIMESTAMP WITH TIME ZONE NOT NULL,
    duration DECIMAL(10,2),
    agent_speech_rate DECIMAL(5,2),
    customer_speech_rate DECIMAL(5,2),
    silence_rate DECIMAL(5,2),
    cross_talk_rate DECIMAL(5,2),
    agent_interrupt_count INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

## File Format

The script expects text files with the following format:
```
AgentName: agent@example.com
PhoneNumber: 05318671534
CallId: dcc558df-8be4-464c-ab19-7f9b3004cee3
StartDate: 24.07.2025 23:03:10
Duration: 713.28
Agent Speech Rate: %14.00
Customer Speech Rate: %40.00
Silence Rate: %0.46
Cross Talk Rate: %0.01
Agent Interrupt Count: 9
```

## Output

The script provides real-time feedback on:
- Files being processed
- Successful imports
- Failed imports
- Final summary with counts

## Error Handling

- Missing required fields are logged as warnings
- Database connection errors are handled gracefully
- File parsing errors are logged and skipped
- Duplicate call IDs are handled with upsert logic
