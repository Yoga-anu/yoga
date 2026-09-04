import mysql.connector

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root@123",
        database="solar_panel_db"
    )

    print("Database Connected Successfully!")

except Exception as e:
    print(e)