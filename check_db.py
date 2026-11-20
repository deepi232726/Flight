import sqlite3

conn = sqlite3.connect("rides.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM rides")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()