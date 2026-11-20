import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="FlightMate@2026",
        database="flightmate"
    )

    print("✅ Database connected successfully")

    cur = conn.cursor()
    cur.execute("SHOW TABLES;")

    for table in cur:
        print(table)

    conn.close()

except Exception as e:
    print("❌ Error:", e)