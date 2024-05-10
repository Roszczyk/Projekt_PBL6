import mysql.connector
import hashlib


def get_hash(string):
    return hashlib.sha256(string.encode()).hexdigest()


def create_users_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL
        )
    """)


def insert_user(cursor, username, password_hash):
    cursor.execute("""
        INSERT INTO users (username, password_hash) 
        VALUES (%s, %s)
    """, (username, password_hash))


def main():
    # MySQL connection configuration
    db_config = {
        'host': '10.141.10.69',
        'port': '3333',
        'user': 'root',
        'password': 'password',
        'database': 'mysql'
    }

    # Connect to MySQL server
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Create the "users" table if it does not exist
        create_users_table(cursor)

        # Insert sample user data
        insert_user(cursor, 'admin', get_hash('admin'))
        insert_user(cursor, 'username', get_hash('password'))

        # Commit changes
        connection.commit()
        print("Users table created and sample data inserted successfully.")

    except mysql.connector.Error as error:
        print("Error:", error)

    finally:
        # Close the cursor and connection
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")


if __name__ == "__main__":
    main()
