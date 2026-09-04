import mysql.connector

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Root@123",   # Replace with your MySQL password
    database="solar_panel_db"
)

cursor = db.cursor()


def save_result(sample_name, defect_class, confidence, ai_response):
    """
    Save YOLO detection result into MySQL database.
    """

    sql = """
    INSERT INTO inspection_results
    (sample_name, defect_class, confidence, ai_response)
    VALUES (%s, %s, %s, %s)
    """

    values = (
        sample_name,
        defect_class,
        confidence,
        ai_response
    )

    cursor.execute(sql, values)
    db.commit()


def close_connection():
    cursor.close()
    db.close()