import sqlite3

conn = sqlite3.connect("rides.db")
cursor = conn.cursor()

users = [
    ("Revathi", "Chennai Airport", "AI202", "10:00"),
    ("Kumar", "Chennai Airport", "6E341", "10:30"),
    ("Madhanika", "Bangalore Airport", "AI876", "12:00"),
    ("Deepika", "Chennai Airport", "UK500", "09:45")
]

cursor.executemany(
    "INSERT INTO rides(name, airport, flight, time) VALUES (?, ?, ?, ?)",
    users
)

conn.commit()
conn.close()

print("Demo data inserted successfully!")