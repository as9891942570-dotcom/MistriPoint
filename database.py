import pymysql

def get_db_connection():
    return pymysql.connect(
        host="pg-2eeb428e-as9891942570-b4ae.i.aivencloud.com",
        port=21960,
        user="avnadmin",
        password="AVNS_ncZYEMIRSIeUob-rnZU",
        database="labour_app",
        ssl={"ssl": {}},
        cursorclass=pymysql.cursors.DictCursor
    )