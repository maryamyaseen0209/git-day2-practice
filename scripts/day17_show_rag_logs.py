#!/usr/bin/env python3
from __future__ import annotations

import sys
import os

# Add the src directory to path
sys.path.insert(0, '/home/maryam205/git-day2-practice/src')

# Set database URL if not set
os.environ['DATABASE_URL'] = 'postgresql://maryam205:maryam205@localhost:5432/git_day_practice'

from git_day_practice.db import SessionLocal
from sqlalchemy import text

def main():
    print("=" * 80)
    print("RAG LOGS - Last 10 Requests")
    print("=" * 80)
    
    try:
        with SessionLocal() as session:
            # Query the logs
            result = session.execute(text("""
                SELECT id, question, action, reason, 
                       top_score, avg_score, result_count,
                       created_at
                FROM rag_logs 
                ORDER BY created_at DESC 
                LIMIT 10
            """))
            
            rows = result.fetchall()
            
            if not rows:
                print("\nNo logs found. Make some RAG requests first!")
                print("\nTry these commands:")
                print("  curl -X POST http://localhost:8000/rag -H 'Content-Type: application/json' -d '{\"question\": \"What is Qdrant?\", \"limit\": 3}'")
                print("  curl -X POST http://localhost:8000/rag -H 'Content-Type: application/json' -d '{\"question\": \"help\", \"limit\": 3}'")
                return
            
            for row in rows:
                print(f"\n{'='*80}")
                print(f"ID: {row[0]}")
                print(f"Question: {row[1][:100]}..." if len(row[1]) > 100 else f"Question: {row[1]}")
                print(f"Action: {row[2]}")
                print(f"Reason: {row[3]}")
                print(f"Top Score: {row[4]:.4f}")
                print(f"Avg Score: {row[5]:.4f}")
                print(f"Result Count: {row[6]}")
                print(f"Created At: {row[7]}")
            
            print(f"\n{'='*80}")
            print(f"Total logs shown: {len(rows)}")
            
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure:")
        print("1. PostgreSQL is running: sudo service postgresql status")
        print("2. The rag_logs table exists")
        print("3. You've made some RAG requests already")

if __name__ == "__main__":
    main()
