import mysql.connector

def connect_to_db():
    connection = mysql.connector.connect(
        host="127.0.0.1:3306",
        user="root",
        password="Naveen@205",
        database="server"
    )
    return connection

# Use this function to execute queries
def execute_query(query, values=None):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()
