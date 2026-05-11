import psycopg2

# Database connection parameters
conn = psycopg2.connect(
    host="localhost",
    database="git_day_practice",
    user="maryam205",
    password="manojazz2005"
)

cur = conn.cursor()

# Get all logs
cur.execute("""
    SELECT id, question, action, reason, created_at, 
           LEFT(answer, 100) as answer_preview
    FROM agent_logs 
    ORDER BY id DESC
""")

rows = cur.fetchall()

print("=" * 80)
print("AGENT LOGS - PostgreSQL Database")
print("=" * 80)

if not rows:
    print("\nNo logs found. Insert sample data with:")
    print("PGPASSWORD='manojazz2005' psql -d git_day_practice -U maryam205 -h localhost -c \"INSERT INTO agent_logs ...\"")
else:
    for row in rows:
        print(f"\nID: {row[0]}")
        print(f"Question: {row[1]}")
        print(f"Action: {row[2]}")
        print(f"Reason: {row[3]}")
        print(f"Created At: {row[4]}")
        print(f"Answer: {row[5]}...")
        print("-" * 50)

cur.close()
conn.close()