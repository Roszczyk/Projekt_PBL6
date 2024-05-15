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


def get_password_hash(username):
    """Retrieve the password hash for the given username from the MySQL database."""
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query = "SELECT password_hash FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result[0] if result else None


def set_recent_user_ip(username, ip):
    """Set the recent IP address and timestamp of the user in the MySQL database."""
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    query = """
    INSERT INTO users_ip (username, recent_ip, timestamp) 
    VALUES (%s, %s, %s) 
    ON DUPLICATE KEY UPDATE 
        recent_ip = VALUES(recent_ip), 
        timestamp = VALUES(timestamp)
    """
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(query, (username, ip, timestamp))

    connection.commit()
    cursor.close()
    connection.close()


@app.route('/check_credentials', methods=['POST'])
def check_credentials():
    """
    Check if the provided username and password are correct.
    ---
    parameters:
      - name: username
        in: formData
        description: The username to check.
        required: true
        type: string
      - name: password
        in: formData
        description: The password to check.
        required: true
        type: string
    responses:
        200:
            description: A response indicating whether the credentials are correct.
            schema:
                type: object
                properties:
                    valid:
                        type: boolean
                        description: Indicates whether the credentials are valid.
    """
    data = request.form
    username = data.get('username')
    password = data.get('password')

    stored_password_hash = get_password_hash(username)

    valid = stored_password_hash is not None and \
        hashlib.sha256(password.encode()).hexdigest() == stored_password_hash

    if valid:
        set_recent_user_ip(username, request.remote_addr)

    return jsonify({'valid': valid})


if __name__ == '__main__':
    app.run(debug=True, port=5001)
