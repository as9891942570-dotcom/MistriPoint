import pymysql

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Ankit@2026",
        database="labour_app",
        cursorclass=pymysql.cursors.DictCursor
    )


