# AuthorizeUser
# Author: PAM

from flask import Flask, jsonify, request
import mysql.connector
import hashlib
import datetime

app = Flask(__name__)

# Database configuration
db_config = {
    'host': '10.141.10.69',
    'port': '3333',
    'user': 'root',
    'password': 'password',
    'database': 'mysql'
}


def get_recent_user_ip(username):
    """Retrieve the recent IP address of the user from the MySQL database."""
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query = "SELECT recent_ip FROM users_ip WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result[0] if result else None


@app.route('/notify', methods=['POST'])
def notify():
    ip = get_recent_user_ip("admin")


if __name__ == '__main__':
    app.run(debug=True, port=5001)
