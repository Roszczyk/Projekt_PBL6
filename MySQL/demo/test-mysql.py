import mysql.connector

# Database configuration
db_config = {
    'host': '10.141.10.69',
    'port': '3333',
    'user': 'root',
    'password': 'password',
    'database': 'mysql'
}


def test_mysql_connection():
    """Test MySQL database connectivity."""
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Connected to MySQL Server version {db_info}")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()[0]
            print(f"Connected to database '{db_name}'")
            cursor.close()
            connection.close()
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL database: {e}")


if __name__ == "__main__":
    test_mysql_connection()
